from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from products.models import (Category, ChainStore, Discount, Product,
                             ProductsInStore, Store, StoreLocation)

User = get_user_model()


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = ('discount_rate', 'discount_unit', 'discount_start', 'discount_end', 'discount_card')


class StoreLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreLocation
        fields = ('id', 'region', 'city', 'street', 'building')


class ChainStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChainStore
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class StoreSerializer(serializers.ModelSerializer):
    location = StoreLocationSerializer()
    chain_store = ChainStoreSerializer()

    class Meta:
        model = Store
        fields = ('id', 'location', 'chain_store', 'name')


class ProductsInStoreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения всех магазинов для конкретного товара."""
    discount = DiscountSerializer(read_only=True)
    store = StoreSerializer(read_only=True)

    class Meta:
        model = ProductsInStore
        fields = ('id', 'discount', 'store', 'price')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для получения товара."""
    category = CategorySerializer()
    stores = ProductsInStoreSerializer(source='product', many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'image', 'stores')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
