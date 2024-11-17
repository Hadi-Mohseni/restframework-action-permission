from rest_framework import serializers
from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    description = serializers.CharField()

    class Meta:
        model = Product
        fields = ["description"]
