from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.serializers import (CategorySerializer, ChainStoreSerializer,
                             ProductSerializer, StoreSerializer)
from products.models import Category, ChainStore, Favorites, Product, Store


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        if request.method == 'POST':
            Favorites.objects.get_or_create(user=user, product=product)
            return Response('Товар успешно добавлен в избранное',
                            status.HTTP_201_CREATED)
        user.favorites.filter(product=product).delete()
        return Response('Товар успешно удален из избранного',
                        status.HTTP_204_NO_CONTENT)

    # TODO
    # новый ендпоинт favorites со списком всех избранных товаров
    # @action(detail=False, methods=['get',])
    # def favorites(self, request, pk=None):
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Response('Недоступно неавторизованным пользователям', status.HTTP_401_UNAUTHORIZED)
    #     else:
    #         self.queryset = Product.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    pagination_class = PageNumberPagination


class ChainStoreViewSet(viewsets.ModelViewSet):
    queryset = ChainStore.objects.all()
    serializer_class = ChainStoreSerializer
    pagination_class = None
