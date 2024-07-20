from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from . import constants
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