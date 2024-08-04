# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from .models import Order

# @receiver(post_save, sender=Order)
# def order_created(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "orders",
#             {
#                 "type": "order_created",
#                 "content": {
#                     "order_id": instance.id,
#                     "user": instance.user.username,
#                     "total_price": str(instance.total_price),
#                     "status": instance.status,
#                 },
#             }
#         )

# myapp/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# @receiver(post_save, sender=Order)
# def send_order_to_admin(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         order_data = {
#             'order_id': instance.id,
#             'user': instance.user.username,
#             'total': instance.total,
#             # Qo'shimcha ma'lumotlar qo'shishingiz mumkin
#         }

#         async_to_sync(channel_layer.group_send)(
#             "admin_orders",
#             {
#                 "type": "new_order",
#                 "order": order_data,
#             }
#         )
