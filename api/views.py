import random
from secrets import randbelow

from django.conf import settings
from django.contrib.auth import get_user_model, hashers
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import AuthorOrReadOnly
from api.serializers import (CategorySerializer, ChainStoreSerializer,
                             CreateProductSerializer,
                             CustomPasswordResetConfirmSerializer,
                             FeedbackSerializer, PinCreateSerializer,
                             ProductSerializer, ReviewSerializer,
                             StoreProductsSerializer, StoreSerializer)
from api.tasks import send_feedback_email
from products.models import (Category, ChainStore, Favorites, Product, Review,
                             Store)
from users.models import ResetPasswordPin

User = get_user_model()


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('category',)
    search_fields = ('=barcode', '@name')
    ordering_fields = ('name', 'category')
    ordering = ('name',)

    def get_queryset(self):
        if self.action == 'favorites':
            return Product.objects.filter(id__in=Favorites.objects.filter(
                user=self.request.user).values('product_id')).annotate(rating=Avg('reviews__score'))
        if self.action == 'random_discounts':
            categories = Category.objects.exclude(name='DIFFERENT')
            products_ids = []
            for category in categories:
                products_in_category = list(Product.objects.filter(category=category))
                random_product = random.choice(products_in_category)
                products_ids.append(random_product.id)
            return Product.objects.filter(id__in=products_ids).annotate(rating=Avg('reviews__score'))
        return Product.objects.annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProductSerializer
        return ProductSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        if request.method == 'POST':
            if Favorites.objects.filter(user=user, product=product).exists():
                return Response('Товар уже есть в Избранном', status.HTTP_422_UNPROCESSABLE_ENTITY)
            Favorites.objects.create(user=user, product=product)
            return Response('Товар успешно добавлен в Избранное', status.HTTP_201_CREATED)
        user_favorite_product = user.favorites.filter(product=product)
        if user_favorite_product.exists():
            user_favorite_product.delete()
            return Response('Товар успешно удален из Избранного', status.HTTP_204_NO_CONTENT)
        return Response('Данный товар не найден в Избранном', status.HTTP_422_UNPROCESSABLE_ENTITY)

    @action(detail=False, methods=['get',])
    def favorites(self, request):
        return super().list(request)

    @action(detail=False, methods=['get',])
    def random_discounts(self, request):
        return super().list(request)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    # FIXME: временно не отдаем на фронт категорию 'Разное', вернемся к этому вопросу позднее
    queryset = Category.objects.exclude(name='DIFFERENT')
    serializer_class = CategorySerializer
    pagination_class = None
    filter_backends = (OrderingFilter,)
    ordering_fields = ('priority',)
    ordering = ('priority',)


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name', 'chain_store')
    ordering = ('chain_store',)


class StoreProductsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StoreProductsSerializer
    pagination_class = PageNumberPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name', 'chain_store',)
    ordering = ('chain_store',)

    def get_queryset(self):
        store_id = self.kwargs.get("store_id")
        if store_id is not None:
            return Store.objects.filter(store=store_id)
        return None


class ChainStoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChainStore.objects.all()
    serializer_class = ChainStoreSerializer
    pagination_class = None
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    ordering = ('name',)


class BaseReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ('-pub_date',)
    ordering = ('-pub_date',)


class ReviewViewSet(BaseReviewViewSet):
    permission_classes = [
        AuthorOrReadOnly & IsAuthenticated
    ]

    def get_product(self):
        return get_object_or_404(Product, id=self.kwargs.get('product_id'))

    def get_queryset(self):
        return self.get_product().reviews.all()

    def perform_create(self, serializer):
        serializer.save(product=self.get_product(), user=self.request.user)


class ResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = []

    def get_serializer(self, *args, **kwargs):
        if self.action == 'confirm':
            return CustomPasswordResetConfirmSerializer(*args, **kwargs)
        if self.action == 'create':
            return PinCreateSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        if self.action == 'create':
            return get_object_or_404(User, **kwargs)
        return super().get_object(*args, **kwargs)

    def create(self, request):
        """Создать и отправить PIN для восстановления пароля пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('username')
        user = self.get_object(username=email)
        pin = ''.join([str(randbelow(10)) for _ in range(4)])
        if ResetPasswordPin.objects.filter(user=user).exists():
            ResetPasswordPin.objects.filter(user=user).delete()
        ResetPasswordPin.objects.create(user=user, pin=hashers.make_password(pin))
        message_mail = send_mail(
            'Восстановление пароля приложения CHERRY',
            settings.RESET_PASSWORD_MESSAGE.format(
                username=user.get_username(),
                pin=pin,
                hostmail=settings.DEFAULT_FROM_EMAIL,
            ),
            settings.DEFAULT_FROM_EMAIL,
            (user.get_username(),),
        )
        if message_mail:
            return Response('Сообщение отправлено', status.HTTP_200_OK)
        return ResetPasswordPin('Сообщение не отправлено', status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def confirm(self, request):
        """Подтверждение сохранения нового пароля пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data.get('user'))
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()
        ResetPasswordPin.objects.filter(user=user).delete()
        send_mail(
            'Пароль успешно изменен',
            settings.DONE_RESET_PASSWORD_MESSAGE,
            settings.DEFAULT_FROM_EMAIL,
            (user.get_username(),),
        )
        return Response('Пароль восстановлен', status.HTTP_200_OK)


class UserReviewsViewSet(BaseReviewViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class FeedbackAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            send_feedback_email.delay(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
