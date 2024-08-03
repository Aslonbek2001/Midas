from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import generics
from rest_framework.filters import SearchFilter
from .models import Product
from .serializers import ProductSerializer
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = CustomPageNumberPagination

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', "available"]
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        discount_not_null = self.request.query_params.get('discount_not_null')
        if discount_not_null:
            queryset = queryset.exclude(discount=None)
        return queryset


