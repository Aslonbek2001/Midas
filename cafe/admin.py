from django.contrib import admin
from .models import Category, Product
import os
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'discount',
        'available',
        'created',
        'updated',
        'hot_cold'
    ]
    list_filter = ['available', 'created', 'updated','discount',]
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
