# Generated by Django 4.2.7 on 2023-12-28 11:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='productsinstore',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='products.discount', verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='productsinstore',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='products.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='productsinstore',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to='products.store', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='Фото товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, help_text='Выберите категорию товара', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='category', to='products.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='product',
            name='stores',
            field=models.ManyToManyField(related_name='stores', through='products.ProductsInStore', to='products.store', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Избранный товар'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('score__range', (1, 5))), name='valid_score'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='score_once'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('product', 'user'), name='unique favorite product'),
        ),
    ]
