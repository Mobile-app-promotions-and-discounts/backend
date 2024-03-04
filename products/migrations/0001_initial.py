# Generated by Django 4.2.7 on 2024-03-04 19:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('PRODUCTS', 'Продукты'), ('CLOTHES', 'Одежда и обувь'), ('HOME', 'Для дома и сада'), ('COSMETICS', 'Косметика и гигиена'), ('KIDS', 'Для детей'), ('ZOO', 'Зоотовары'), ('AUTO', 'Авто'), ('HOLIDAYS', 'К празднику'), ('DIFFERENT', 'Разное')], default='PRODUCTS', max_length=9, verbose_name='Название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/', verbose_name='Иконка категории')),
                ('priority', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Приоритет категории в дизайн-макете')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ChainStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название сети магазинов')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='store_logos/', verbose_name='Логотип сети')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Сайт сети магазинов')),
            ],
            options={
                'verbose_name': 'Сеть магазинов',
                'verbose_name_plural': 'Сети магазинов',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_rate', models.IntegerField(verbose_name='Размер скидки')),
                ('discount_unit', models.CharField(choices=[('RUB', 'Скидка в рублях'), ('%', 'Скидка в процентах')], default='%', max_length=3, verbose_name='Единица измерения')),
                ('discount_start', models.DateField(verbose_name='Начало акции')),
                ('discount_end', models.DateField(verbose_name='Окончание акции')),
                ('discount_card', models.BooleanField(default=False, verbose_name='Скидка по карте')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
                'ordering': ('discount_rate',),
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
                'ordering': ('product',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('barcode', models.CharField(blank=True, max_length=15, null=True, verbose_name='Штрихкод')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='product_images/', verbose_name='Главное изображение продукта')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(unique=True, upload_to='product_images/', verbose_name='Дополнительное изображение товара')),
            ],
            options={
                'verbose_name': 'Изображение товар',
                'verbose_name_plural': 'Изображения товара',
            },
        ),
        migrations.CreateModel(
            name='ProductsInStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_price', models.CharField(max_length=10, verbose_name='Цена товара без акции')),
                ('promo_price', models.CharField(max_length=10, verbose_name='Цена товара по акции')),
            ],
            options={
                'verbose_name': 'Скидка на товар в магазине',
                'verbose_name_plural': 'Скидки на товар в магазине',
            },
        ),
        migrations.CreateModel(
            name='StoreLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=100, verbose_name='Регион')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('latitude', models.CharField(max_length=100, verbose_name='Широта')),
                ('longitude', models.CharField(max_length=100, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Адрес магазина',
                'verbose_name_plural': 'Адреса магазинов',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('id_in_chain_store', models.CharField(blank=True, max_length=6, null=True, verbose_name='id магазина в сети')),
                ('chain_store', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='chain_store', to='products.chainstore', verbose_name='Сеть магазинов')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='products.storelocation', verbose_name='Адрес магазина')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Поделитесь своим мнением о товаре', verbose_name='Текст отзыва')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка товара')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления отзыва')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.product', verbose_name='Ссылка на товар')),
            ],
            options={
                'verbose_name': 'Отзыв на товар',
                'verbose_name_plural': 'Отзывы на товары',
            },
        ),
    ]
