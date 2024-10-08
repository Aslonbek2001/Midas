from .models import Product, Category
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta
import random
from rest_framework import exceptions


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer
    class Meta:
        model = Product
        fields = '__all__'

class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, help_text="Qidiruv so'zi")