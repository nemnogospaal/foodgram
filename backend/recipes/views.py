from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import AuthorOrReadOnly
from api.utils import create_pdf
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from recipes.serializers import (FavoriteRecipeSerializer,
                                 IngredientSerializer, PostRecipeSerializer,
                                 RecipeSerializer, TagSerialzier)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return PostRecipeSerializer

    def get_queryset(self):
        queryset = self.queryset
        is_favorite = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')

        if is_favorite:
            queryset = queryset.filter(in_favorite__user=self.request.user)

        if is_in_shopping_cart:
            queryset = queryset.filter(shopping_cart__user=self.request.user)

        return queryset

    @staticmethod
    def post_recipe(related_model, user, pk):
        if related_model.objects.filter(recipe_id=pk, user=user).exists():
            return Response(
                'Рецепт уже добавлен в избранное',
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        related_model.objects.create(recipe=recipe, user=user)
        serializer = FavoriteRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_recipe(related_model, user, pk):
        if related_model.objects.filter(recipe_id=pk, user=user).exists():
            related_model.objects.filter(recipe_id=pk, user=user).delete()
            return Response('Рецепт удалён из избранных',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(
            'Такого рецепта нет',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, *args, **kwargs):
        user = self.request.user
        if self.request.method == 'POST':
            return self.post_recipe(Favorite, user, self.kwargs['pk'])
        return self.delete_recipe(Favorite, user, self.kwargs['pk'])

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, *args, **kwargs):
        user = self.request.user
        if self.request.method == 'POST':
            return self.post_recipe(ShoppingCart, user, self.kwargs['pk'])
        return self.delete_recipe(ShoppingCart, user, self.kwargs['pk'])

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(amount=Sum('amount'))
        return create_pdf(ingredients)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerialzier
