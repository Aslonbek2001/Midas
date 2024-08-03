from django.db import models
from users.models import ClientModel


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    stripe_charge_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.amount} {self.currency}'
    
