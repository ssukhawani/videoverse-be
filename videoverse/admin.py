from django.contrib import admin
from .models import Video

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploader', 'name', 'file_path', 'file_size', 'mime_type', 'upload_date')
    list_filter = ('mime_type',)
    ordering= ('-upload_date',)

admin.site.register(Video, VideoAdmin)
