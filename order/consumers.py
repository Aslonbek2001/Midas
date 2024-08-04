# # # consumers.py
# # from channels.generic.websocket import AsyncWebsocketConsumer
# # import json
# # from datetime import datetime
# # from asgiref.sync import async_to_sync
# # from channels.generic.websocket import WebsocketConsumer


# # class OrderConsumer(AsyncWebsocketConsumer):
# #     async def connect(self):
# #         print("=========OrderConsumer.   connect ============")
# #         await self.channel_layer.group_add(
# #             "orders",  # Bu guruhni yaratib unga ulaning
# #             self.channel_name
# #         )
# #         await self.accept()

# #     async def disconnect(self, close_code):
# #         print(f"=========OrderConsumer. {close_code}  disconnect ============")
# #         await self.channel_layer.group_discard(
# #             "orders",  # Guruhdan uzilish
# #             self.channel_name
# #         )

# #     async def receive(self, text_data):
# #         print("=========OrderConsumer.   receive ============")
# #         print(f"============{text_data}==========")
# #         pass  # Ma'lumotlarni olish uchun ishlatiladi, bu erda kerak emas

# #     async def order_created(self, event):
        
# #         # Buyurtma yaratildi, frontendga ma'lumot yuborish
# #         await self.send(text_data=json.dumps(event["content"]))


# # #################################################################

# # class OrderConsumer(WebsocketConsumer):
# #     def connect(self):
# #         self.group_name = "orders"
# #         async_to_sync(self.channel_layer.group_add)(
# #             self.group_name,
# #             self.channel_name
# #         )
# #         self.accept()

# #     def disconnect(self, close_code):
# #         async_to_sync(self.channel_layer.group_discard)(
# #             self.group_name,
# #             self.channel_name
# #         )

# #     def order_message(self, event):
# #         print(f"=========={event}=========")
# #         print("=========OrderConsumer.   receive ============")
# #         message = event['message']

# #         self.send(text_data=json.dumps({
# #             'message': message
# #         }))

# # myapp/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class OrderConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Barcha adminlar bir xil guruhga ulanadi
#         self.group_name = "admin_orders"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         pass  # Odatda clientlardan ma'lumot qabul qilish kerak emas

#     async def new_order(self, event):
#         await self.send(text_data=json.dumps(event))
