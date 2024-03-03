from django.core.validators import MinValueValidator
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента в рецепте."""

    id = serializers.IntegerField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'name',
            'amount',
            'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class TagSerialzier(serializers.ModelSerializer):
    """Сериализатор тега."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного рецепта."""

    class Meta:
        model = Favorite
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта."""

    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        read_only=True,
        source='ingredient_amount')
    image = Base64ImageField(required=True)
    tags = TagSerialzier(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user.id
        recipe = obj.id
        return Favorite.objects.filter(user_id=user,
                                       recipe_id=recipe).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user.id
        recipe = obj.id
        return ShoppingCart.objects.filter(user_id=user,
                                           recipe_id=recipe).exists()


class PostRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецепта."""

    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = IngredientInRecipeSerializer(many=True, required=True)
    image = Base64ImageField(required=True)
    cooking_time = serializers.IntegerField(
        required=True,
        validators=[
            MinValueValidator(
                1,
                'Время приготовления должно быть больше одной минуты')
        ])

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data

    def validate(self, data):
        if not data.get('tags'):
            raise ValidationError('Необходимо выбрать теги')
        if not data.get('ingredients'):
            raise ValidationError('Необходимо выбрать ингредиенты')
        return data

    def validate_image(self, image):
        if not image:
            raise ValidationError(
                'Необходимо добавить картинку'
            )
        return image

    def validate_ingredients(self, ingredients):
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            raise ValidationError(
                'Ингредиенты должны быть уникальными'
            )
        if not ingredients:
            raise ValidationError(
                'Необходимо выбрать ингредиенты'
            )
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise ValidationError(
                'Необходимо выбрать теги'
            )
        if len(tags) != len(set(tags)):
            raise ValidationError(
                'Теги должны быть уникальными'
            )
        return tags

    def add_ingredients(self, recipe, ingredients):
        IngredientAmount.objects.bulk_create([IngredientAmount(
            ingredient=ingredient['id'],
            recipe=recipe,
            amount=ingredient['amount']
        ) for ingredient in ingredients])

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.add_ingredients(instance, ingredients)
        return super().update(instance, validated_data)


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранного рецепта."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(CustomUserSerializer):
    """Сериализатор подписки на пользователя."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Follow.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                'Подписка уже оформлена'
            )
        if user == author:
            raise ValidationError(
                'Невозможно оформить подписку на себя'
            )
        return data

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj)
        if recipes_limit:
            recipes = Recipe.objects.filter(
                author=obj).order_by('-id')[:int(recipes_limit)]
        serializer = FavoriteRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
