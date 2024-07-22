# core/permissions.py
from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'superadmin'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['superadmin', 'admin']

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'user'
