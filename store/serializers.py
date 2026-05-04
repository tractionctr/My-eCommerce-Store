"""REST API serializers for store models."""

from rest_framework import serializers
from .models import Product, Store, Review


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    class Meta:
        model = Product
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Store model."""
    class Meta:
        model = Store
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    class Meta:
        model = Review
        fields = '__all__'
