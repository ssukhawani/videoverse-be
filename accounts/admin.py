from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserLimit

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'id','full_name', 'role','is_verified', 'is_staff', 'is_superuser', 'is_active','auth_provider')
    list_filter = ('is_staff', 'is_superuser', 'role','is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('role','is_verified', 'is_staff', 'is_superuser', 'is_active','auth_provider',"groups",
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


class UserLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'limit_name', 'limit_value')
    list_filter = ('limit_name',)
    search_fields = ('user__full_name', 'limit_name')
    change_form_template = 'admin/change_form.html'

admin.site.register(UserLimit, UserLimitAdmin)