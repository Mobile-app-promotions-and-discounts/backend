from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('stores', views.StoreViewSet)
router.register('chains', views.ChainStoreViewSet)

urlpatterns = [
    path('',include(router.urls)),

]
