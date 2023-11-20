from rest_framework import viewsets

from products.models import Category
from api.serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
