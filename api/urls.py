from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, ChainStoreViewSet, FeedbackAPIView,
                    NearestShopsView, ProductViewSet, ResetPasswordViewSet,
                    ReviewViewSet, StoreProductsViewSet, StoreViewSet,
                    UserLocationView, UserReviewsViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('products', ProductViewSet, basename='products')
router.register(r'products/(?P<product_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register('categories', CategoryViewSet, basename='categories')
router.register('stores', StoreViewSet, basename='stores')
router.register(r'stores/(?P<store_id>\d+)/products', StoreProductsViewSet, basename='store-products')
router.register('chains', ChainStoreViewSet, basename='chains')
router.register('reset-password', ResetPasswordViewSet, basename='reset-password')
router.register('my-reviews', UserReviewsViewSet, basename='my-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback'),
    path('nearest-shops/', NearestShopsView.as_view(), name='nearest-shops'),
    path('user-location/', UserLocationView.as_view(), name='user-location'),
]
