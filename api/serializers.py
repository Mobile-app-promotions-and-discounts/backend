from rest_framework import serializers

from products.models import (Category, ChainStore, Discount, Product,
                             ProductsInStore, Store, StoreLocation)


class DiscountSerializer(serializers.ModelSerializer):
    """Cериализатор для получения информации о скидке."""

    class Meta:
        model = Discount
        fields = ('discount_rate', 'discount_unit', 'discount_start', 'discount_end', 'discount_card')


class StoreLocationSerializer(serializers.ModelSerializer):
    """Cериализатор для получения адреса магазина."""

    class Meta:
        model = StoreLocation
        fields = ('id', 'region', 'city', 'street', 'building')


class ChainStoreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о сети магазинов."""

    class Meta:
        model = ChainStore
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    """Cериализатор для получения краткой информации о категории."""

    class Meta:
        model = Category
        fields = ('id', 'name')


class StoreSerializer(serializers.ModelSerializer):
    """Cериализатор для получения краткой информации о магазине."""
    location = StoreLocationSerializer()
    chain_store = ChainStoreSerializer()

    class Meta:
        model = Store
        fields = ('id', 'location', 'chain_store', 'name')


class ProductsInStoreSerializer(serializers.ModelSerializer):
    """Cериализатор для получения цены и скидки на конкретный товар."""
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


class ProductCurrentStoreSerializer(serializers.ModelSerializer):
    """Cериализатор для получения цены и скидки на конкретный товар."""
    discount = DiscountSerializer()
    product = serializers.StringRelatedField()

    class Meta:
        model = ProductsInStore
        fields = ("id", "price", "product", "discount")


class StoreLongSerializer(serializers.ModelSerializer):
    """Сериализатор для получения магазинов и товаров в них."""
    products = ProductCurrentStoreSerializer(source='store', many=True)

    class Meta:
        model = Store
        fields = ('id', 'location', 'chain_store', 'name', 'products')


class ProductInCategorySerializer(serializers.ModelSerializer):
    """Cериализатор для получения товаров по категориям."""
    class Meta:
        model = Product
        fields = ("id", "name", "description", "image")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для получения товаров по категориям."""

    products = ProductInCategorySerializer(source='category', many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'products')
