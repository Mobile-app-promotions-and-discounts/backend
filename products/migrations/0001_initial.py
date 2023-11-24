# Generated by Django 4.2.7 on 2023-11-24 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ChainStore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, verbose_name="Название сети магазинов"
                    ),
                ),
            ],
            options={
                "verbose_name": "Сеть магазинов",
                "verbose_name_plural": "Сети магазинов",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Discount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("discount_rate", models.IntegerField(verbose_name="Размер скидки")),
                (
                    "discount_unit",
                    models.CharField(
                        choices=[
                            ("RUB", "Скидка в рублях"),
                            ("%", "Скидка в процентах"),
                        ],
                        default="%",
                        max_length=11,
                        verbose_name="Единица измерения",
                    ),
                ),
                (
                    "discount_start",
                    models.CharField(max_length=50, verbose_name="Начало акции"),
                ),
                (
                    "discount_end",
                    models.CharField(max_length=50, verbose_name="Окончание акции"),
                ),
                (
                    "discount_card",
                    models.BooleanField(default=False, verbose_name="Скидка по карте"),
                ),
            ],
            options={
                "verbose_name": "Скидка",
                "verbose_name_plural": "Скидки",
                "ordering": ("discount_rate",),
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "category",
                    models.ForeignKey(
                        default="Без категории",
                        help_text="Выберите категорию товара",
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        related_name="category",
                        to="products.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "main_image",
                    models.ImageField(
                        upload_to="product_images", verbose_name="Главное изображение"
                    ),
                ),
                (
                    "additional_photo",
                    models.ImageField(
                        upload_to="product_images",
                        verbose_name="Дополнительное изображение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение",
                "verbose_name_plural": "Изображения",
            },
        ),
        migrations.CreateModel(
            name="StoreLocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("region", models.CharField(max_length=100, verbose_name="Регион")),
                ("city", models.CharField(max_length=100, verbose_name="Город")),
                ("street", models.CharField(max_length=255, verbose_name="Улица")),
                (
                    "building",
                    models.CharField(max_length=20, verbose_name="Номер здания"),
                ),
            ],
            options={
                "verbose_name": "Адрес магазина",
                "verbose_name_plural": "Адреса магазинов",
            },
        ),
        migrations.CreateModel(
            name="Store",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "chain_store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chain_store",
                        to="products.chainstore",
                        verbose_name="Сеть магазинов",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="location",
                        to="products.storelocation",
                        verbose_name="Адрес магазина",
                    ),
                ),
            ],
            options={
                "verbose_name": "Магазин",
                "verbose_name_plural": "Магазины",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ProductsInStore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.FloatField()),
                (
                    "discount",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discount",
                        to="products.discount",
                        verbose_name="Скидка",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product",
                        to="products.product",
                        verbose_name="Товар",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="store",
                        to="products.store",
                        verbose_name="Магазин",
                    ),
                ),
            ],
            options={
                "verbose_name": "Скидка на товар в магазине",
                "verbose_name_plural": "Скидки на товар в магазине",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="image",
                to="products.productimage",
                verbose_name="Изображение товара",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="stores",
            field=models.ManyToManyField(
                related_name="stores",
                through="products.ProductsInStore",
                to="products.store",
                verbose_name="Магазин",
            ),
        ),
    ]
