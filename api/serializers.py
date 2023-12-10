import base64
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from products.models import (Category, ChainStore, Discount, Product,
                             ProductsInStore, Review, Store, StoreLocation)

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class DiscountSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о скидке."""

    class Meta:
        model = Discount
        fields = ('discount_rate', 'discount_unit', 'discount_start', 'discount_end', 'discount_card')


class StoreLocationSerializer(serializers.ModelSerializer):
    """Сериализатор для получения адреса магазина."""

    class Meta:
        model = StoreLocation
        fields = ('id', 'region', 'city', 'street', 'building')


class ChainStoreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о сети магазинов."""

    class Meta:
        model = ChainStore
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для получения краткой информации о категории."""

    class Meta:
        model = Category
        fields = ('id', 'name')


class StoreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения краткой информации о магазине."""
    location = StoreLocationSerializer()
    chain_store = ChainStoreSerializer()

    class Meta:
        model = Store
        fields = ('id', 'location', 'chain_store', 'name')


class ProductsInStoreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения цены и скидки на конкретный товар."""
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
    rating = serializers.FloatField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'rating', 'category', 'barcode', 'description', 'image', 'stores', 'is_favorited')

    def get_is_favorited(self, obj):
        user_requsting = self.context['request'].user
        if not user_requsting.is_authenticated:
            return False
        return user_requsting.favorites.filter(product=obj).exists()


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


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""
    foto = Base64ImageField(required=False, allow_null=True)


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для получения цены и скидки на конкретный товар."""
    discount = DiscountSerializer()
    product = serializers.StringRelatedField()

    class Meta:
        model = ProductsInStore
        fields = ("id", "price", "product", "discount")


class StoreProductsSerializer(serializers.ModelSerializer):
    """Сериализатор для получения магазинов и товаров в них."""
    products = ProductDetailSerializer(source='store', many=True)

    class Meta:
        model = Store
        fields = ('id', 'chain_store', 'name', 'location', 'products')
