from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        db_index=True,
        max_length=60,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=15,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name='Ингредиент'
        verbose_name_plural='Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]
    
    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега'
    )
    color = ColorField(
        unique=True,
        verbose_name='Цветовой код'
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг'
    )
    
    class Meta:
        verbose_name='Тег'
        verbose_name_plural='Теги'
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    """Модель избранного рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='media/',
        verbose_name='Картинка'
    )
    text = models.CharField(
        max_length=1000,
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(
        default=1,
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


    def __str__(self):
        return self.name

class Favorite(models.Model):
    """Модель избранного рецепта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


    def __str__(self):
        return f'{self.user} {self.recipe}'



class ShoppingCart(models.Model):
    """Модель корзины покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shopping_list'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class IngredientAmount(models.Model):
    """Модель количества ингредиентов в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_amount'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amount',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Необходимо количество больше единицы')
            ]
        )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.recipe} {self.ingredient}'