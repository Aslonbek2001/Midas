import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Product

@receiver(post_delete, sender=Product)
def delete_image_on_delete(sender, instance, **kwargs):
    """
    Model instance o'chirilganda unga tegishli rasmni o'chiradi.
    """
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
