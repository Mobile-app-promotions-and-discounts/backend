from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.serializers import (CategorySerializer, ChainStoreSerializer,
                             ProductSerializer, ReviewSerializer,
                             StoreProductsSerializer, StoreSerializer)
from products.models import (Category, ChainStore, Favorites, Product, Review,
                             Store)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',)

    def get_queryset(self):
        if self.action == "favorites":
            return Product.objects.filter(id__in=Favorites.objects.filter(user=self.request.user).values('product_id'))
        return Product.objects.annotate(rating=Avg('reviews__score'))

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        if request.method == 'POST':
            Favorites.objects.get_or_create(user=user, product=product)
            return Response('Товар успешно добавлен в избранное', status.HTTP_201_CREATED)
        user.favorites.filter(product=product).delete()
        return Response('Товар успешно удален из избранного', status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get',])
    def favorites(self, request):
        return super().list(request)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    pagination_class = PageNumberPagination


class StoreProductsViewSet(viewsets.ModelViewSet):
    serializer_class = StoreProductsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        store_id = self.kwargs.get("store_id")
        if store_id is not None:
            return Store.objects.filter(store=store_id)
        return None


class ChainStoreViewSet(viewsets.ModelViewSet):
    queryset = ChainStore.objects.all()
    serializer_class = ChainStoreSerializer
    pagination_class = None


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    queryset = Review.objects.all()

    def get_product(self):
        return get_object_or_404(Product, id=self.kwargs.get('product_id'))

    def get_queryset(self):
        return self.get_product().reviews.all()

    def perform_create(self, serializer):
        serializer.save(product=self.get_product(), customer=self.request.user)
