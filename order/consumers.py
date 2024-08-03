# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "orders",  # Bu guruhni yaratib unga ulaning
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "orders",  # Guruhdan uzilish
            self.channel_name
        )

    async def receive(self, text_data):
        pass  # Ma'lumotlarni olish uchun ishlatiladi, bu erda kerak emas

    async def order_created(self, event):
        # Buyurtma yaratildi, frontendga ma'lumot yuborish
        await self.send(text_data=json.dumps(event["content"]))

