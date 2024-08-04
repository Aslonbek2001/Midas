from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_order_created(order):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "orders",  # Guruh nomi
        {
            "type": "order_message",
            "message": f"New order created: {order.id}"
        }
    )
