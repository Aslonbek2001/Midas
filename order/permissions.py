from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Foydalanuvchi faqat o'z buyurtmalarini ko'ra va o'zgartira oladi,
    adminlar esa faqat yangilay oladi.
    """

    def has_object_permission(self, request, view, obj):
        # Read permission - barcha foydalanuvchilar ko'rishi mumkin
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permission - foydalanuvchi faqat o'z buyurtmasini o'zgartirishi mumkin
        if request.user.is_staff:
            return True

        return obj.user == request.user