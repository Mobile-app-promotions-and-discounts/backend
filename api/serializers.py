from rest_framework import serializers

from products.models import (Category, ChainStore, Discount, Product,
                             ProductsInStore, Store, StoreLocation)


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
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'image', 'stores', 'is_favorited')

    def get_is_favorited(self, obj):
        user_requsting = self.context['request'].user
        if not user_requsting.is_authenticated:
            return False
        return user_requsting.favorites.filter(product=obj).exists()
