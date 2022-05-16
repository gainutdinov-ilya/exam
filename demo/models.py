from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import validate_email
from django.db import models

from demo.validators import *


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=128,
        validators=[
            validate_email
        ]
    )

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
        blank=True,
        validators=[validate_cyr_only]
    )

    password = models.CharField(
        verbose_name='Пароль',
        max_length=256,
        validators=[validate_password],

    )

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    REQUIRED_FIELDS = ['email', 'name', 'surname', 'password']

    def __str__(self):
        return f"{self.name} {self.surname} {self.patronymic}"


class Category(models.Model):
    label = models.CharField(
        verbose_name='Название',
        max_length=64
    )

    def __str__(self):
        return f"{self.label}"


class Product(models.Model):
    label = models.CharField(
        verbose_name='Название',
        max_length=64
    )

    description = models.CharField(
        verbose_name='Описание',
        max_length=128
    )

    count = models.IntegerField(
        verbose_name='На складе'
    )

    category = models.ForeignKey(
        verbose_name="Категория",
        to=Category,
        on_delete=models.CASCADE
    )

    img = models.ImageField(
        verbose_name='Изображение'
    )

    price = models.FloatField(
        verbose_name='Цена'
    )

    date = models.DateField(
        verbose_name='Дата добавления',
        auto_now=True,
        auto_created=True
    )

    def __str__(self):
        return f"{self.label} на складе {self.count} ед."

    def dec(self, count=1):
        self.count -= count
        self.save()

    def inc(self, count=1):
        self.count += count
        self.save()


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

    description = models.CharField(
        max_length=512,
        verbose_name='Описание'
    )

    def __str__(self):
        return f"{self.product.label} {self.count} ед"

    def dec(self, count=1):
        self.count -= count
        self.save()

    def inc(self, count=1):
        self.count += count
        self.save()

    def get_by_user(self, user):
        return self.objects.all().filter(user=user)


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

    def compare_to_order(self) -> Order:
        order = Order(
            items=self.items,
            user=self.user
        )
        self.delete()
        order.save()
        return order

    def add_item(self, product_pk):
        product = Product.objects.get(pk=product_pk)
        try:
            cart_item = self.items.objects.get(product=product)
        except Product.DoesNotExists:
            cart_item = None
        if not cart_item:
            cart_item = CartItem(product=product, price=product.price, count=1)
            cart_item.save()
            self.items.objects.add(cart_item)
        else:
            cart_item.inc()

    def del_item(self, product_pk):
        product = Product.objects.get(pk=product_pk)
        cart_item = self.items.objects.get(product=product)
        cart_item.remove()
