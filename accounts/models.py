from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db.models import UniqueConstraint
from .managers import CustomUserManager
from . import constants
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum
import uuid


# Create your models here.
AUTH_PROVIDERS = {'email':'email', 'google':'google'}


class Role(models.TextChoices):
    SUPER_ADMIN = constants.SUPER_ADMIN, 'Super Admin'
    ADMIN = constants.ADMIN, 'Admin'
    USER = constants.USER, 'User'
        
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider =  models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def get_full_name(self):
        return self.full_name

@receiver(post_save, sender=CustomUser)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == Role.ADMIN:
            admin_group, created = Group.objects.get_or_create(name='Admin')
            instance.groups.add(admin_group)
        elif instance.role == Role.SUPER_ADMIN:
            # Ensure that superuser and staff fields are set correctly
            instance.is_superuser = True
            instance.is_staff = True
            instance.save()

class Limit(models.TextChoices):
    UPLOAD_SIZE_LIMIT = "UPLOAD_SIZE_LIMIT", "upload_size_limit"
    UPLOAD_NUMBER_LIMIT = "UPLOAD_NUMBER_LIMIT", "upload_number_limit"
    STORAGE_QUOTA = "STORAGE_QUOTA", "storage_quota"
    DAILY_UPLOAD_LIMIT = "DAILY_UPLOAD_LIMIT", "daily_upload_limit"
    MONTHLY_UPLOAD_LIMIT = "MONTHLY_UPLOAD_LIMIT", "monthly_upload_limit"
    CONCURRENT_UPLOADS_LIMIT = "CONCURRENT_UPLOADS_LIMIT", "concurrent_uploads_limit"

class Unit(models.TextChoices):
    KB = "KB", "KB"
    MB = "MB", "MB"
    GB = "GB", "GB"
    NUMBER = "NUMBER", "NUMBER"
    
class UserLimit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='limits', db_index=True)
    limit_name = models.CharField(max_length=50, choices=Limit.choices)
    limit_value = models.PositiveIntegerField(help_text=(
        'Enter the limit value. Units:<br>'
        '- upload_size_limit: mb<br>'
        '- upload_number_limit: number of uploads<br>'
        '- storage_quota: mb<br>'
        '- daily_upload_limit: number of uploads<br>'
        '- monthly_upload_limit: number of uploads<br>'
        '- concurrent_uploads_limit: number of concurrent uploads'
    ))
    unit = models.CharField(max_length=50, choices=Unit.choices)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'limit_name'], name='unique_user_limit')
        ]
    def __str__(self):
        return f'{self.limit_name} for {self.user.full_name}: {self.limit_value}'