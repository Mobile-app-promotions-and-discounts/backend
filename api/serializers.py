from rest_framework import serializers
from products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')
        model = Category
