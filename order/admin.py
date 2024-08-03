# from django.contrib import admin
# from .models import Order, OrderItem
# # Register your models here.

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ["user", "status", "order_date"]

# @admin.register(OrderItem)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['product', 'quantity', 'price']

# admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Qo'shimcha bo'sh forma
    fields = ['product', 'quantity', 'price']  # Ko'rsatiladigan maydonlar

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'user', 'total_price', 'status', 'order_date']
    search_fields = ['user__username']  # Foydalanuvchi username bo'yicha qidiruv

admin.site.register(Order, OrderAdmin)
