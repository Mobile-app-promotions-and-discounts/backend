from django.core.validators import MaxValueValidator
from django.db import models


class Product(models.Model):
    """Модель продукта/товара."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        'Category',
        related_name='category',
        on_delete=models.SET_DEFAULT,
        default='Без категории'
    )
    price = models.FloatField()
    image = models.ForeignKey(
        'ProductImage',
        related_name='image',
        on_delete=models.CASCADE
    )
    store = models.ManyToManyField(
        'Store',
        through='ProductsInStore',
        related_name='store'
    )


class Category(models.Model):
    """Модель категории, к которой относится товар."""
    name = models.CharField(max_length=255)


class ProductImage(models.Model):
    """Модель фотографий товара."""
    main_image = models.ImageField(
        upload_to='product_images',
        blank=True,
        null=True
    )
    additional_photo = models.ImageField(
        upload_to='product_images',
        blank=True,
        null=True
    )


class Store(models.Model):
    """Модель единичного магазина (физический объект на карте)."""
    name = models.CharField(max_length=255)
    location = models.ForeignKey(
        'StoreLocation',
        related_name='location',
        on_delete=models.CASCADE
    )
    # url = models.URLField()
    chain_store = models.ForeignKey(
        'ChainStore',
        related_name='chain_store',
        on_delete=models.SET_NULL,
        null=True
    )


class ProductsInStore(models.Model):
    """Модель для связи таблиц Product и Store."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE
    )
    discount = models.ForeignKey(
        'Discount',
        related_name='discount',
        on_delete=models.SET_NULL,
        null=True
    )
    # url = models.URLField()


class Discount(models.Model):
    """Модель акции/скидки."""
    discount_rate = models.IntegerField()
    discount_unit = models.BigIntegerField()
    discount_rating = models.IntegerField()
    discount_start = models.DateTimeField(auto_now_add=True)
    discount_end = models.DateTimeField(auto_now_add=True)
    discount_card = models.BooleanField(default=False)


class StoreLocation(models.Model):
    """Модель для адреса конкретного магазина."""
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    building = models.PositiveSmallIntegerField()
    postal_index = models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)]
    )


class ChainStore(models.Model):
    """Модель для сети магазинов."""
    name = models.CharField(max_length=100)
