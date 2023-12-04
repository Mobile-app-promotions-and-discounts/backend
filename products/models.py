from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Product(models.Model):
    """Модель продукта/товара."""
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    barcode = models.CharField('Штрихкод', max_length=13)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name='category',
        verbose_name='Категория',
        help_text='Выберите категорию товара'
    )
    image = models.ForeignKey(
        'ProductImage',
        related_name='image',
        on_delete=models.CASCADE,
        verbose_name='Изображение товара'
    )
    stores = models.ManyToManyField(
        'Store',
        through='ProductsInStore',
        related_name='stores',
        verbose_name='Магазин'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории, к которой относится товар."""
    name = models.CharField('Название', max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Модель фотографий товара."""
    main_image = models.ImageField(
        'Главное изображение',
        upload_to='product_images',
        blank=True,
        null=True
    )
    additional_photo = models.ImageField(
        'Дополнительное изображение',
        upload_to='product_images',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Store(models.Model):
    """Модель единичного магазина (физический объект на карте)."""
    name = models.CharField('Название', max_length=255)
    location = models.ForeignKey(
        'StoreLocation',
        related_name='location',
        on_delete=models.CASCADE,
        verbose_name='Адрес магазина'
    )
    chain_store = models.ForeignKey(
        'ChainStore',
        related_name='chain_store',
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name='Сеть магазинов'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return f'{self.name} по адресу {self.location}'


class ProductsInStore(models.Model):
    """Модель для связи таблиц Product и Store."""
    product = models.ForeignKey(
        Product,
        related_name='product',
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    store = models.ForeignKey(
        Store,
        related_name='store',
        on_delete=models.CASCADE,
        verbose_name='Магазин'
    )
    price = models.FloatField('Цена')
    discount = models.ForeignKey(
        'Discount',
        related_name='discount',
        on_delete=models.CASCADE,
        verbose_name='Скидка'
    )

    class Meta:
        verbose_name = 'Скидка на товар в магазине'
        verbose_name_plural = 'Скидки на товар в магазине'

    def __str__(self):
        return f'{self.product.name} в {self.store}'


class Discount(models.Model):
    """Модель акции/скидки."""
    RUBLES = 'RUB'
    PERCENTAGE = '%'

    UNIT_CHOICES = [
        (RUBLES, 'Скидка в рублях'),
        (PERCENTAGE, 'Скидка в процентах'),
    ]

    discount_rate = models.IntegerField('Размер скидки')
    discount_unit = models.CharField(
        'Единица измерения',
        max_length=11,
        choices=UNIT_CHOICES,
        default=PERCENTAGE,
    )
    discount_start = models.DateField('Начало акции')
    discount_end = models.DateField('Окончание акции')
    discount_card = models.BooleanField('Скидка по карте', default=False)

    class Meta:
        ordering = ('discount_rate',)
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'Скидка в размере {self.discount_rate} {self.discount_unit}'


class StoreLocation(models.Model):
    """Модель для адреса конкретного магазина."""
    region = models.CharField('Регион', max_length=100)
    city = models.CharField('Город', max_length=100)
    street = models.CharField('Улица', max_length=255)
    building = models.CharField('Номер здания', max_length=20)

    class Meta:
        verbose_name = 'Адрес магазина'
        verbose_name_plural = 'Адреса магазинов'

    def __str__(self):
        return f'{self.city}, {self.street}, {self.building}'


class ChainStore(models.Model):
    """Модель для сети магазинов."""
    name = models.CharField('Название сети магазинов', max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Сеть магазинов'
        verbose_name_plural = 'Сети магазинов'

    def __str__(self):
        return f'Сеть {self.name}'


class Favorites(models.Model):
    "Модель для избранных товаров"
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Избранный товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites',
                             verbose_name='Пользователь')

    class Meta:
        ordering = ('product',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [models.UniqueConstraint(fields=['product', 'user'], name='unique favorite product')]

    def __str__(self):
        return f'{self.user.username}`s favorite product {self.product.name}'


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Ссылка на товар'
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Покупатель'
    )
    text = models.TextField(
        help_text='Поделитесь своим мнением о товаре',
        verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка товара'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв на товар'
        verbose_name_plural = 'Отзывы на товары'

    def __str__(self):
        return self.text[:30]
