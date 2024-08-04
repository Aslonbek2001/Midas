from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CategoryListCreateView, CategoryDetailView, SearchView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('category/', CategoryListCreateView.as_view(), name='product-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='product-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]