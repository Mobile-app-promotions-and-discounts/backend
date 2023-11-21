from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register('discounts', views.DiscountViewSet)#, basename='tags')
router.register('products', views.ProductViewSet)
#router.register('ingredients', views.IngredientViewSet, basename='ingredients')
#router.register('users', views.UserViewSet)

urlpatterns = [
    path('',include(router.urls)),

]
