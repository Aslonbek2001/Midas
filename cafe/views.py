from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import generics
from rest_framework.filters import SearchFilter
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, SearchSerializer
from .pagination import CustomPageNumberPagination
from .permissions import  IsStaffPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class SearchView(generics.GenericAPIView):
    serializer_class = SearchSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data['query']

        # Qidiruvni barcha modellarda amalga oshirish
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        categories = Category.objects.filter(Q(name__icontains=query))

        data = {
            'products': ProductSerializer(products, many=True).data,
            'categories': CategorySerializer(categories, many=True).data,
        }
        
        return Response(data, status=status.HTTP_200_OK)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'available', 'famous', 'hot_cold']
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status']
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]



