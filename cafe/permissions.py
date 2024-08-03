from rest_framework import permissions
from rest_framework.permissions import BasePermission

# class IsAuthorOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.rule == "AU"

class IsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        # Foydalanuvchi is_staff bo'lishi kerak
        return request.user and request.user.is_staff