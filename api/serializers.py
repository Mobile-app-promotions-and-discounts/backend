from rest_framework import serializers

from products.models import (Product, ProductsInStore, Discount, 
                             Store, StoreLocation, ChainStore,
                             Category)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class StoreLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreLocation
        fields = '__all__'

class ChainStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainStore
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    location = StoreLocationSerializer()
    chain_store = ChainStoreSerializer()
    class Meta:
        model = Store
        fields = ('id', 'location', 'chain_store', 'name')

class ProductsInStoreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения всех магазинов для конкретного товара."""
    id = serializers.ReadOnlyField()
    discount = DiscountSerializer(read_only=True)
    stores = StoreSerializer(read_only=True)

    class Meta:
        model = ProductsInStore
        fields = ('id', 'price', 'discount', 'stores')

class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для получения товара."""
    category = CategorySerializer()
    store = ProductsInStoreSerializer(many=True, source='product')

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'image', 'rating', 'store')

