from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser, Role

@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == Role.ADMIN:
            admin_group, created = Group.objects.get_or_create(name='Admin')
            instance.groups.add(admin_group)
        elif instance.role == Role.SUPER_ADMIN:
            instance.is_superuser = True
            instance.is_staff = True
            instance.save()
