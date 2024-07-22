from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'videos/{instance.uploader.id}/{filename}'

class Video(models.Model):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=200)
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure file_path is set before saving
        if self.file and not self.file_path:
            # Generate the path using Django's storage system
            path = user_directory_path(self, self.file.name)
            # Use default_storage to get the available name
            full_file_path = default_storage.generate_filename(path)
            self.file_path = full_file_path
        super().save(*args, **kwargs)