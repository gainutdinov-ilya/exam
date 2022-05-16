from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from demo.validators import *


# Create your models here.

class User(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        max_length=32,
        validators=[validate_eng_only_with_numeric],
        unique=True
    )

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

    password = models.CharField(
        verbose_name='Пароль',
        max_length=256,
        validators=[validate_password]
    )

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    REQUIRED_FIELDS = ['name', 'surname']

    def __str__(self):
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
        to=Category,
        on_delete=models.CASCADE
    )

    img = models.ImageField(
        verbose_name='Изображение'
    )


class CartItem(models.Model):
    product = models.ForeignKey(
        to=Product,
        verbose_name='Товар',
        on_delete=models.CASCADE
    )

    count = models.IntegerField(
        verbose_name='Единиц товара'
    )

    price = models.FloatField(
        verbose_name='Цена на момент покупки'
    )


class Order(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE
    )

    items = models.ManyToManyField(
        verbose_name='Товары',
        to=CartItem
    )

    orderTime = models.DateTimeField(
        auto_now=True,
        auto_created=True,
        verbose_name='Время заказа'
    )


class Cart(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE
    )

    items = models.ManyToManyField(
        verbose_name='Товары',
        to=CartItem
    )

    def CompareToOrder(self) -> Order:
        order = Order(
            items=self.items,
            user=self.user
        )
        self.delete()
        order.save()
        return order
