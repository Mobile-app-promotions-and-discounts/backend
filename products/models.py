from django.db import models


class Product(models.Model):
    """Модель продукта/товара."""
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    category = models.ForeignKey(
        'Category',
        related_name='category',
        on_delete=models.SET_DEFAULT,
        default='Без категории',
        verbose_name='Категория',
        help_text='Выберите категорию товара'
    )
    image = models.ForeignKey(
        'ProductImage',
        related_name='image',
        on_delete=models.CASCADE,
        blank = True, null = True
        verbose_name='Изображение товара'
    )
    store = models.ManyToManyField(
        'Store',
        through='ProductsInStore',
        related_name='store',
        verbose_name='Магазин'
    )
    rating = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории, к которой относится товар."""
    name = models.CharField('Название', max_length=255)

    class Meta:
        ordering = ("name",)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

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
        verbose_name='Локация'
    )
    chain_store = models.ForeignKey(
        'ChainStore',
        related_name='chain_store',
        on_delete=models.CASCADE
   #   on_delete=models.SET_NULL,
        null=True,
        verbose_name='Сеть магазинов'
    )

    class Meta:
        ordering = ("name",)
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
    stores = models.ForeignKey(
        Store,
        related_name='stores',
        on_delete=models.CASCADE,
        verbose_name='Магазин'
    )
    price = models.FloatField()
    discount = models.ForeignKey(
        'Discount',
        related_name='discount',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Скидка'
    )

    class Meta:
        verbose_name = 'Скидка на товар в магазине'
        verbose_name_plural = 'Скидки на товар в магазине'


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
    discount_start = models.DateTimeField('Время начало скидки')
    discount_end = models.DateTimeField('Время окончание скидки')
    discount_card = models.BooleanField('Скидочная карта', default=False)

    class Meta:
        ordering = ("discount_rate",)
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'Скидка в размере {self.discount_rate} {self.discount_unit}'


class StoreLocation(models.Model):
    """Модель для адреса конкретного магазина."""
    region = models.CharField('Регион', max_length=100)
    city = models.CharField('Город', max_length=100)
    street = models.CharField('Улица', max_length=255)
    building = models.CharField('Номер дома', max_length=10)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'город {self.city}, улица {self.street} {self.building}'

    def __str__(self):
        return f'{self.city}, {self.street}, {self.building}'


class ChainStore(models.Model):
    """Модель для сети магазинов."""
    name = models.CharField('Название', max_length=100)

    class Meta:
        ordering = ("name",)
        verbose_name = 'Сеть магазинов'
        verbose_name_plural = 'Сети магазинов'

    def __str__(self):
        return f'Сеть {self.name}'
