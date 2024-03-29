import base64
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib.auth import get_user_model, hashers
from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.validators import username_validation
from products.models import (Category, ChainStore, Discount, Product,
                             ProductImage, ProductsInStore, Review, Store,
                             StoreLocation)
from users.models import ResetPasswordPin

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
        fields = ('image',)


class DiscountSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о скидке."""

    class Meta:
        model = Discount
        fields = ('discount_rate', 'discount_unit', 'discount_start', 'discount_end', 'discount_card')


class StoreLocationSerializer(serializers.ModelSerializer):
    """Сериализатор для получения адреса магазина."""

    class Meta:
        model = StoreLocation
        fields = ('id', 'region', 'city', 'address')


class ChainStoreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о сети магазинов."""

    class Meta:
        model = ChainStore
        fields = ('id', 'name', 'logo', 'website')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для получения краткой информации о категории."""

    class Meta:
        model = Category
        fields = ('id', 'priority', 'get_name_display', 'image')


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
        fields = ('id', 'discount', 'store', 'initial_price', 'promo_price')


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Review
        fields = ('id', 'product_id', 'product_name', 'user', 'text', 'score', 'pub_date')

    def validate_score(self, value):
        """Валидация для оценки товара."""
        if not (0 < value <= 5):
            raise serializers.ValidationError(
                'Оценка должна быть целым числом от 1 до 5.'
            )
        return value

    def validate(self, data):
        """Валидация для создания отзыва."""
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        product_id = self.context['request'].parser_context['kwargs']['product_id']
        if Review.objects.filter(user=user, product=product_id).exists():
            raise serializers.ValidationError('Нельзя оставить больше одного отзыва.')
        return data


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для получения товара."""
    category = CategorySerializer()
    stores = ProductsInStoreSerializer(source='product', many=True)
    is_favorited = serializers.SerializerMethodField()
    rating = serializers.FloatField()
    images = ImageProductsSerialiser(
        many=True,
        read_only=True,
    )
    my_review = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'rating', 'category', 'barcode', 'description',
                  'main_image', 'stores', 'is_favorited', 'images', 'my_review')

    def get_my_review(self, obj):
        user = self.context['request'].user
        review = Review.objects.filter(product=obj, user=user).first()
        if review is not None:
            return {'id': review.id, 'text': review.text, 'score': review.score}
        return None

    def get_is_favorited(self, obj):
        user_requsting = self.context['request'].user
        if not user_requsting.is_authenticated:
            return False
        return user_requsting.favorites.filter(product=obj).exists()


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
            if Product.objects.filter(product, image=image.get('image')).exists():
                continue
            ProductImage.objects.create(
                product=product,
                image=image.get('image'),
            )
        return product


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""
    photo = Base64ImageField(required=False, allow_null=True)


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для получения цены и скидки на конкретный товар."""
    discount = DiscountSerializer()
    product = serializers.StringRelatedField()

    class Meta:
        model = ProductsInStore
        fields = ('id', 'initial_price', 'promo_price', 'product', 'discount')


class StoreProductsSerializer(serializers.ModelSerializer):
    """Сериализатор для получения магазинов и товаров в них."""
    products = ProductDetailSerializer(source='store', many=True)

    class Meta:
        model = Store
        fields = ('id', 'chain_store', 'name', 'location', 'products')


class CustomPasswordResetConfirmSerializer(serializers.ModelSerializer):
    """Сериалайзер подтверждения сброса пароля пользователя по PIN."""
    user = serializers.EmailField()
    new_password = serializers.CharField()

    class Meta:
        model = ResetPasswordPin
        fields = ('user', 'pin', 'new_password')

    def validate_user(self, value):
        return username_validation(value)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        username = data.get('user')
        pin = data.get('pin')
        if not ResetPasswordPin.objects.filter(user__username=username).exists():
            raise ValidationError(f'Не найден PIN сброса пароля для {username}')
        obj_in_db = ResetPasswordPin.objects.get(user__username=username)
        life_time = datetime.now(tz=ZoneInfo('UTC')) - obj_in_db.create_date
        if life_time > timedelta(minutes=settings.LIFE_TIME_PIN):
            raise ValidationError('Время жизни PIN истекло')
        if not hashers.check_password(pin, obj_in_db.pin):
            raise ValidationError('PIN не валиден')
        return data


class PinCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер создания PIN для сброса пароля пользователя."""
    username = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username',)

    def validate_username(self, value):
        return username_validation(value)


class FeedbackSerializer(serializers.Serializer):
    """Сериализатор для получения обратной связи от пользователя."""
    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(
        max_length=100,
        required=True,
    )
    message = serializers.CharField(max_length=3000, required=True)
    image_file = serializers.CharField(required=False, allow_null=True)

    def validate_image_file(self, value):
        if not value.startswith('data:image'):
            raise serializers.ValidationError(
                'Изображение должно быть в формате base64'
            )
        return value
