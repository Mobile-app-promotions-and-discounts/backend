from django.urls import include, path
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CategoryViewSet, StoreViewSet, ChainStoreViewSet

app_name = 'api'

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('stores', StoreViewSet)
router.register('chains', ChainStoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
