from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'id','full_name', 'role','is_verified', 'is_staff', 'is_superuser', 'is_active','auth_provider')
    list_filter = ('is_staff', 'is_superuser', 'role','is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_verified', 'is_staff', 'is_superuser', 'is_active','auth_provider',"groups",
                    "user_permissions",)}),
    )
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
        ('Permissions', {'fields': ('is_verified', 'is_staff', 'is_superuser', 'is_active')}),
    )
    list_per_page = 20

admin.site.register(CustomUser, CustomUserAdmin)
