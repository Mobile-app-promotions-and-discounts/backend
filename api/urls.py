from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, ChainStoreViewSet, ProductViewSet,
                    ReviewViewSet, StoreViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register(r'products/(?P<product_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register('categories', CategoryViewSet, basename='categories')
router.register('stores', StoreViewSet, basename='stores')
router.register('chains', ChainStoreViewSet, basename='chains')

urlpatterns = [
    path('', include(router.urls)),
]
