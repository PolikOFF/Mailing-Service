from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='номер телефона', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', null=True, blank=True)
    country = models.CharField(max_length=35, verbose_name='страна', null=True, blank=True)

    token = models.CharField(max_length=10, verbose_name='токен верификации', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ("set_is_active", "Активация пользователя")
        ]
