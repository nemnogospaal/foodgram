from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import USERNAME_SYMBOLS_REGEX


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        validators=[USERNAME_SYMBOLS_REGEX,],
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
    
    def __str__(self):
        return self.username
    
class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='user_following')]
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'    

    def __str__(self):
        return f'{self.user} {self.author}'

