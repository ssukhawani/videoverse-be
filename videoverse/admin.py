from django.contrib import admin
from .models import Video, TrimmedVideo, MergedVideo

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploader', 'name', 'file_path', 'file_size', 'mime_type', 'upload_date')
    list_filter = ('mime_type',)
    ordering= ('-upload_date',)

admin.site.register(Video, VideoAdmin)

@admin.register(TrimmedVideo)
class TrimmedVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'original_video', 'file_path', 'file_size', 'start_time', 'end_time', 'created_at')
    list_filter = ('user', 'original_video', 'created_at')
    search_fields = ('user__username', 'original_video__name', 'file_path')
    readonly_fields = ('created_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('file_path', 'file_size',)
        return self.readonly_fields

@admin.register(MergedVideo)
class MergedVideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_path', 'file_size', 'created_at')
    search_fields = ('file_path', 'user__username')