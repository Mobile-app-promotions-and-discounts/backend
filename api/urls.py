from django.urls import path, include
from rest_framework import routers

from api.views import CategoryViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'category', CategoryViewSet)


urlpatterns = [
    path('', include(v1_router.urls)),
]
