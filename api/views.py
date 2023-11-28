from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import (CategorySerializer, ChainStoreSerializer,
                             ProductSerializer, StoreSerializer)
from products.models import Category, ChainStore, Product, Store


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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
