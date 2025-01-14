from rest_framework import permissions
from .models import User

class IsBusinessOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == User.UserType.BUSINESS_OWNER

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == User.UserType.ADMIN

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == User.UserType.ADMIN:
            return True
        return obj.id == request.user.id