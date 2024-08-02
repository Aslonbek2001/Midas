from django.contrib import admin
from .models import ClientModel, VerificationCode
# Register your models here.

@admin.register(ClientModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', "email", "phone"]
    
@admin.register(VerificationCode)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user", "code"]
