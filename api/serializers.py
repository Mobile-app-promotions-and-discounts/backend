from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from products.models import (Category, ChainStore, Discount, Product,
                             ProductImage, ProductsInStore, Review, Store,
                             StoreLocation)

User = get_user_model()


class ImageProductsSerialiser(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image')


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
    rating = serializers.FloatField()
    images = ImageProductsSerialiser(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'rating', 'category', 'description', 'main_image', 'stores', 'images')


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'description', 'barcode', 'category', 'main_image', 'store', 'images')

    def create(self, validated_data):
        category = validated_data.pop('category')
        store = validated_data.pop('store')
        images = validated_data.pop('images')

        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('customer', 'text', 'score', 'pub_date')

    def validate_review(self, value):
        """Валидация для оценки рейтинга."""
        if not (0 < value <= 5):
            raise serializers.ValidationError(
                'Рейтинг должен быть целым числом от 0 до 5.'
            )
        return value


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
