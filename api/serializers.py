import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import (Category, ChainStore, Discount, Product,
                             ProductImage, ProductsInStore, Review, Store,
                             StoreLocation)

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ImageProductsSerialiser(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ProductImage
        fields = ('image',) #'id', 'product', 


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
    main_image = Base64ImageField()
    images = ImageProductsSerialiser(many=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'barcode', 'category', 'main_image', 'images')

    def create(self, validated_data):
        category = validated_data.pop('category')
        images = validated_data.pop('images')
        if not Category.objects.filter(name=category).exists():
            raise ValidationError('Задана несуществующая категория')
        product = Product.objects.create(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            barcode=validated_data.get('barcode'),
            category=Category.objects.get(name=category),
            main_image=validated_data.get('main_image'),
        )
        for image in images:
            # проверить наличие этой картинки для этого товара
            ProductImage.objects.create(
                product=product,
                image=image.get('image'),
            )
        return product


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
