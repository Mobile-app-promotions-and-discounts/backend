from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Product(models.Model):
    """Модель продукта/товара."""
    name = models.CharField('Название', max_length=255)
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    barcode = models.CharField(
        'Штрихкод',
        max_length=13,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name='category',
        verbose_name='Категория',
        help_text='Выберите категорию товара'
    )
    main_image = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True,
        verbose_name='Главное изображение продукта',
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
    class CategoryType(models.TextChoices):
        PRODUCTS = 'PRODUCTS', 'Продукты'
        CLOTHES = 'CLOTHES', 'Одежда и обувь'
        HOME = 'HOME', 'Для дома и сада'
        COSMETICS = 'COSMETICS', 'Косметика и гигиена'
        KIDS = 'KIDS', 'Для детей'
        ZOO = 'ZOO', 'Зоотовары'
        AUTO = 'AUTO', 'Авто'
        HOLIDAYS = 'HOLIDAYS', 'К празднику'

    name = models.CharField('Название', max_length=9, choices=CategoryType.choices, default=CategoryType.PRODUCTS)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Модель фотографий товара."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Фото товара',
    )
    image = models.ImageField(
        upload_to='product_images/',
        unique=True,
        verbose_name='Дополнительное изображение товара',
    )

    class Meta:
        verbose_name = 'Изображение товар'
        verbose_name_plural = 'Изображения товара'


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
    initial_price = models.IntegerField('Цена товара без акции')
    promo_price = models.IntegerField('Цена товара по акции')
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
    class UnitType(models.TextChoices):
        RUBLES = 'RUB', 'Скидка в рублях'
        PERCENTAGE = '%', 'Скидка в процентах'

    discount_rate = models.IntegerField('Размер скидки')
    discount_unit = models.CharField(
        'Единица измерения',
        max_length=3,
        choices=UnitType.choices,
        default=UnitType.PERCENTAGE,
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
    address = models.CharField('Адрес', max_length=100)
    lat = models.CharField('Широта', max_length=100)
    long = models.CharField('Долгата', max_length=100)

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
