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
    image = models.ForeignKey(
        'ProductImage',
        related_name='image',
        on_delete=models.CASCADE,
        blank = True, null = True
    )
    store = models.ManyToManyField(
        'Store',
        through='ProductsInStore',
        related_name='store'
    )
    rating = models.IntegerField()

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории, к которой относится товар."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} по адресу {self.location}'


class ProductsInStore(models.Model):
    """Модель для связи таблиц Product и Store."""
    product = models.ForeignKey(
        Product,
        related_name='product',
        on_delete=models.CASCADE
    )
    stores = models.ForeignKey(
        Store,
        related_name='stores',
        on_delete=models.CASCADE
    )
    price = models.FloatField()
    discount = models.ForeignKey(
        'Discount',
        related_name='discount',
        on_delete=models.CASCADE
    )
    # url = models.URLField()


class Discount(models.Model):
    """Модель акции/скидки."""
    discount_rate = models.IntegerField()
  #  discount_unit = models.BigIntegerField()
  #  discount_rating = models.IntegerField()
  #  discount_start = models.DateTimeField(auto_now_add=True)
  #  discount_end = models.DateTimeField(auto_now_add=True)
    discount_card = models.BooleanField(default=False)

    def __str__(self):
        return f'Скидка {self.discount_rate} %'


class StoreLocation(models.Model):
    """Модель для адреса конкретного магазина."""
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    building = models.PositiveSmallIntegerField()
    postal_index = models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)]
    )

    def __str__(self):
        return f'{self.city}, {self.street}, {self.building}'


class ChainStore(models.Model):
    """Модель для сети магазинов."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Сеть {self.name}'
