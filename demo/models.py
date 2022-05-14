from django.contrib.auth.models import AbstractUser
from django.db import models

from validators import *


# Create your models here.

class User(AbstractUser):
    name = models.CharField(
        verbose_name='Имя',
        max_length=32,
        validators=[validate_cyr_only]
    )

    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=32,
        validators=[validate_cyr_only],
    )

    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=32,
        blank=False,
        validators=[validate_cyr_only]
    )

    login = models.CharField(
        verbose_name='Логин',
        max_length=32,
        validators=[validate_eng_only],
        unique=True
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=64
    )

    USERNAME_FIELD = login

    def __str(self):
        return f"{self.name} {self.surname} {self.patronymic}"

class Category(models.Model):
    label = models.CharField(
        verbose_name='Название',
        max_length=64
    )

class Product(models.Model):
    label = models.CharField(
        verbose_name='Название',
        max_length=64
    )

    description = models.CharField(
        verbose_name='Описание',
        max_length=128
    )

    category = models.ForeignKey(
        verbose_name="Категория",
        to=Category
    )

    img = models.ImageField(
        verbose_name='Изображение'
    )

class CartItem(models.Model):
    product = models.ForeignKey(
        to=Product,
        verbose_name='Товар'
    )

    count = models.IntegerField(
        verbose_name='Единиц товара'
    )

    price = models.FloatField(
        verbose_name='Цена на момент покупки'
    )

class Cart(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User
    )

    items = models.ManyToManyField(
        to=CartItem,
        verbose_name='Товары'
    )