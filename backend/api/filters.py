from django_filters import CharFilter, FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceField(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

        def get_is_favorited(self, value, queryset):
            request = self.context['request']
            if request.user.is_authenticated and value is True:
                return queryset.filter(in_favorite__user=self.request.user)
            return queryset

        def get_is_in_shopping_cart(self, value, queryset):
            request = self.context['request']
            if request.user.is_authenticated and value is True:
                return queryset.filter(shopping_cart__user=self.request.user)
            return queryset
