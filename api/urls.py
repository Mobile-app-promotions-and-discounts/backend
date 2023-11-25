from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, ChainStoreViewSet, ProductViewSet,
                    StoreLongViewSet, StoreShortViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('stores', StoreShortViewSet)
router.register('stores-with-products', StoreLongViewSet)
router.register('chains', ChainStoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
