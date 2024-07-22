from rest_framework import serializers
from .models import Video, TrimmedVideo

class VideoSerializer(serializers.ModelSerializer):
    file_path = serializers.CharField(required=False, read_only=True)
    
    class Meta:
        model = Video
        fields = ['file', 'name', 'file_path']

class VideoRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'name', 'file_path', 'file_size', 'mime_type', 'upload_date']
        
class TrimmedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrimmedVideo
        fields = ['id', 'file_path', 'file_size', 'start_time', 'end_time', 'created_at', 'name']