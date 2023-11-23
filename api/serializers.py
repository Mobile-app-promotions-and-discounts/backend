from rest_framework import serializers

from products.models import (
    Category, ChainStore, Discount, Product,
    ProductsInStore, Store, StoreLocation
)


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
    discount = DiscountSerializer()
    stores = StoreSerializer()
    price = serializers.ReadOnlyField()

    class Meta:
        model = ProductsInStore
        fields = ('id', 'discount', 'stores', 'price')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для получения товара."""
    category = CategorySerializer()
    store = ProductsInStoreSerializer(source='product')

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'image', 'store')

    def get_store(self, obj):
        store = ProductsInStore.objects.filter(store=obj)
        return ProductsInStoreSerializer(store, many=True).data
