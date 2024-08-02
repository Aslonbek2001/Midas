from .models import Product, Category
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta
import random
from rest_framework import exceptions


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        feilds = ("name", "slug")



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'