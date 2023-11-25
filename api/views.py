from products.models import Category, ChainStore, Product, Store
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import (CategorySerializer, ChainStoreSerializer,
                             ProductSerializer, StoreLongSerializer,
                             StoreShortSerializer)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class StoreShortViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreShortSerializer
    pagination_class = PageNumberPagination


class StoreLongViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreLongSerializer
    pagination_class = PageNumberPagination


class ChainStoreViewSet(viewsets.ModelViewSet):
    queryset = ChainStore.objects.all()
    serializer_class = ChainStoreSerializer
    pagination_class = None
