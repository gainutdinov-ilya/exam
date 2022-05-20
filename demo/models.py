from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
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

    REQUIRED_FIELDS = ['email', 'name', 'surname']

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

    description = models.CharField(
        max_length=512,
        verbose_name='Описание'
    )

    def __str__(self):
        return f"{self.pk} {self.label} на складе {self.count} ед."

    def dec(self, count=1):
        self.count -= count
        self.save()

    def inc(self, count=1):
        self.count += count
        self.save()


class Order(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE
    )

    items = models.ManyToManyField(
        verbose_name='Товары',
        to=Product,
        through='OrderItem',
        through_fields=('order', 'product'),
        related_name='items'
    )

    orderTime = models.DateTimeField(
        auto_now=True,
        auto_created=True,
        verbose_name='Время заказа'
    )

    rejection_reason = models.CharField(
        verbose_name='Причина отмены',
        max_length=512,
        blank=True
    )

    status = models.CharField(
        verbose_name='Статус',
        choices=(
            ('new', 'Новый'),
            ('end', 'Завершён'),
            ('canceled', 'Отменён')
        ),
        max_length=8,
        default='new'
    )

    def get_count(self):
        count = 0
        for item in self.orderitem_set.all():
            count += item.count
        return count

    def __str__(self):
        return f"{self.user.name} {self.user.surname} | Товаров в заказе: {self.get_count()} | Статус: {self.get_status_display()}"

    def get_by_user(user):
        try:
            order = Order.objects.all().filter(user=user)
        except ObjectDoesNotExist:
            return None
        return order


class OrderItem(models.Model):
    product = models.ForeignKey(
        to=Product,
        verbose_name='Товар',
        on_delete=models.CASCADE
    )

    order = models.ForeignKey(
        verbose_name='Заказ',
        to=Order,
        on_delete=models.CASCADE
    )

    count = models.IntegerField(
        verbose_name='Единиц товара'
    )

    price = models.FloatField(
        verbose_name='Цена на момент покупки'
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

    def __str__(self):
        return f"{self.pk} {self.product.label} {self.count} ед"

    def dec(self, count=1):
        self.count -= count
        self.save()

    def inc(self, count=1):
        self.count += count
        self.save()

    def get_by_user(self, user):
        return self.objects.all().filter(user=user)


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

    def get_by_user(user):
        try:
            cart = Cart.objects.get(user=user)
        except ObjectDoesNotExist:
            cart = Cart(user=user)
            cart.save()
        return cart

    def compare_to_order(self) -> Order:
        order = Order(
            user=self.user
        )
        order.save()
        for item in self.items.all():
            order_item = OrderItem(
                product=item.product,
                price=item.product.price,
                count=item.count,
                order=order
            )
            order_item.save()
            item.delete()
            order.orderitem_set.add(order_item)

        return order

    def add_item(self, product_pk) -> CartItem:
        product = Product.objects.get(pk=product_pk)
        try:
            cart_item = self.items.get(product=product)
        except ObjectDoesNotExist:
            cart_item = None
        if not cart_item:
            cart_item = CartItem(product=product, count=1)
            cart_item.save()
            self.items.add(cart_item)
        else:
            cart_item.inc()
        return cart_item

    def del_item(self, product_pk) -> CartItem:
        product = Product.objects.get(pk=product_pk)
        try:
            cart_item = self.items.get(product=product)
        except ObjectDoesNotExist:
            cart_item = None
        if not cart_item:
            cart_item = CartItem(product=product, count=1)
            cart_item.save()
            self.items.add(cart_item)
        else:
            cart_item.dec()
        if cart_item.count == 0:
            cart_item.delete()
            return None
        return cart_item
