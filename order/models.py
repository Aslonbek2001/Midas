from django.db import models
from cafe.models import Product, Category
from users.models import ClientModel


# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('canceled', 'Canceled'),
#     ]
#     user = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="orders")
#     product = models.ManyToManyField(Product) 
#     quantity = models.PositiveIntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     order_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    PAYMENT_CHOICES = [
        ('card', 'card'),
        ('cash', 'Cash'),
    ]
    PAYMENT_STATUS = [
        ('paid', 'Paid'),
        ('unpaid', 'unpaid'),
    ]
    user = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=4, choices=PAYMENT_CHOICES, default='card')
    payment_status = models.CharField(max_length=6, choices=PAYMENT_STATUS, default='unpaid')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.id} for Order {self.order.id}"