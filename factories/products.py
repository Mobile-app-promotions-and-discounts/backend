import os

from datetime import timedelta
from decimal import Decimal

import factory.fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

from products.models import (Category, ChainStore, Discount, Favorites,
                             Product, ProductImage, ProductsInStore, Review,
                             Store, StoreLocation)

from .constants import CHAIN_STORES, PRODUCTS_NAMES, PRODUCTS_DESCRIPTIONS
from .users import UserFactory

fake = Faker(locale='ru_RU')

absolute_path = os.path.dirname(__file__)
relative_path = "categories_images"
PATH = os.path.join(absolute_path, relative_path)


class ChainStoreFactory(DjangoModelFactory):
    class Meta:
        model = ChainStore
        django_get_or_create = ('name',)

    name = factory.Iterator(CHAIN_STORES)
    logo = factory.django.ImageField(color=factory.Faker('color'))


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Iterator(Category.CategoryType.values)
    image = factory.django.ImageField(color=factory.Faker('color'))


class StoreLocationFactory(DjangoModelFactory):
    class Meta:
        model = StoreLocation

    region = factory.Faker('region', locale='ru_RU')
    city = factory.Faker('city', locale='ru_RU')
    street = factory.Faker('street_name', locale='ru_RU')
    building = factory.Faker('building_number', locale='ru_RU')


class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.Faker('text', max_nb_chars=10, locale='ru_RU')
    location = factory.SubFactory(StoreLocationFactory)
    chain_store = factory.SubFactory(ChainStoreFactory)


class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = Discount

    discount_rate = factory.Faker('pyint', min_value=1, max_value=100)
    discount_unit = factory.Iterator(Discount.UnitType.values)
    discount_start = factory.LazyAttribute(lambda _: fake.date_this_month(after_today=True))
    discount_end = factory.LazyAttribute(lambda _self: _self.discount_start + timedelta(days=30))
    discount_card = factory.Faker('boolean', chance_of_getting_true=10)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('name',)

    name = factory.Iterator(PRODUCTS_NAMES)
    description = factory.Iterator(PRODUCTS_DESCRIPTIONS)
    barcode = factory.LazyAttribute(lambda _: fake.ean(length=13))
    category = factory.SubFactory(CategoryFactory)
    main_image = factory.django.ImageField(color=factory.Faker('color'))


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = factory.django.ImageField(color=factory.Faker('color'))


class ProductsInStoreFactory(DjangoModelFactory):
    class Meta:
        model = ProductsInStore

    product = factory.SubFactory(ProductFactory)
    store = factory.SubFactory(StoreFactory)
    initial_price = factory.fuzzy.FuzzyDecimal(low=10.0, high=1000.0)
    discount = factory.SubFactory(DiscountFactory)
    promo_price = factory.LazyAttribute(
        lambda x: x.initial_price - x.discount.discount_rate if x.discount.discount_unit == 'RUB'
        else x.initial_price - x.initial_price * (Decimal(str(x.discount.discount_rate / 100))))


class ProductWithStoreFactory(ProductFactory):
    stores = factory.RelatedFactory(ProductsInStoreFactory, factory_related_name='product')


class FavoritesFactory(DjangoModelFactory):
    class Meta:
        model = Favorites

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)


class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Faker('text', max_nb_chars=50, locale='ru_RU')
    score = factory.Faker('pyint', min_value=1, max_value=5)
    pub_date = factory.LazyAttribute(lambda _: fake.date_this_month(before_today=False))
