from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import generics
from rest_framework.filters import SearchFilter
from .models import Product
from .serializers import ProductSerializer
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = CustomPageNumberPagination

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthorOrReadOnly]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']


