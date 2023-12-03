from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import (CategorySerializer, ChainStoreSerializer,
                             ProductSerializer, ReviewSerializer,
                             StoreSerializer)
from products.models import Category, ChainStore, Product, Review, Store


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    queryset = Review.objects.all()

    def get_product(self):
        return get_object_or_404(Product, id=self.kwargs.get('product_id'))

    def get_queryset(self):
        return self.get_product().reviews.all()
