from django.db import models
import os

class Category(models.Model):
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    STATE_CHOICES = [
        ('hot', 'Hot'),
        ('cold', 'cold'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    hot_cold = models.CharField(max_length=4, choices=STATE_CHOICES, null=True, blank=True)
    famous = models.BooleanField(default=False)
    weight = models.IntegerField(verbose_name="Product og'irligi")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['discount']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Rasmni o'chirish
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super(Product, self).delete(*args, **kwargs)

    def get_price(self):
        if self.discount:
            return self.price - self.discount
        return self.price