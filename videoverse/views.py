import os
import datetime
import subprocess
import uuid

from django.http import JsonResponse
from django.conf import settings
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import Video, TrimmedVideo, MergedVideo
from .serializers import VideoSerializer, VideoRetrieveSerializer, TrimmedVideoSerializer, MergedVideoSerializer

DEFAULT_DAILY_UPLOAD_LIMIT = 20
DEFAULT_MAX_UPLOAD_SIZE_MB = 1000
DEFAULT_STORAGE_QUOTA_MB = 2000

class UserVideoListView(generics.ListAPIView):
    serializer_class = VideoRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Video.objects.filter(uploader=user)

class VideoUploadView(generics.CreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user = self.request.user
        file = self.request.FILES.get('file')
        name = self.request.data.get('name')
        
        print(self.request.data)
        
        if file:
            file_size = file.size
            mime_type = file.content_type
            if not self.check_upload_limits(user, file_size):
                raise DRFValidationError({"detail": "Upload limits exceeded",})

            
            # Save video instance
            serializer.save(
                uploader=user, 
                file_size=file_size,
                mime_type=mime_type,
                name=name
            )
        
    def get_file_path(self, user_id, filename):
        # Define a path for each user's files
        user_directory = f'videos/{user_id}/'
        return os.path.join(user_directory, filename)
    
    def check_upload_limits(self, user, file_size):
        # Implement the logic to check upload limits
        # Retrieve limits or set defaults
        size_limit = user.limits.filter(limit_name='upload_size_limit').first()
        size_limit_value = size_limit.limit_value if size_limit else DEFAULT_MAX_UPLOAD_SIZE_MB * 1024 * 1024  # 100 MB default

        if file_size > size_limit_value:
            return False
        
        # Check total storage quota
        storage_quota = user.limits.filter(limit_name='storage_quota').first()
        storage_quota_value = storage_quota.limit_value if storage_quota else DEFAULT_STORAGE_QUOTA_MB * 1024 * 1024  # 1000 MB default
        total_size = Video.objects.filter(uploader=user).aggregate(total_size=models.Sum('file_size'))['total_size'] or 0

        if total_size + file_size > storage_quota_value:
            return False
        
        # Check daily upload limit
        daily_limit = user.limits.filter(limit_name='daily_upload_limit').first()
        daily_limit_value = daily_limit.limit_value if daily_limit else DEFAULT_DAILY_UPLOAD_LIMIT
        today_uploads = Video.objects.filter(
            uploader=user,
            upload_date__date=datetime.date.today()
        ).count()
        if today_uploads >= daily_limit_value:
            return False
        
        # Check monthly upload limit
        monthly_limit = user.limits.filter(limit_name='monthly_upload_limit').first()
        if monthly_limit:
            this_month_uploads = Video.objects.filter(
                uploader=user,
                upload_date__month=datetime.date.today().month,
                upload_date__year=datetime.date.today().year
            ).count()
            if this_month_uploads >= monthly_limit.limit_value:
                return False
        
        return True

def get_thumbnail_interval(file_size):
    # Define thresholds and intervals in bytes and seconds
    if file_size < 100 * 1024 * 1024:  # Less than 100 MB
        return 20  # Interval of 5 seconds
    elif file_size < 500 * 1024 * 1024:  # Between 100 MB and 500 MB
        return 60  # Interval of 10 seconds
    elif file_size < 1000 * 1024 * 1024:  # Between 500 MB and 1 GB
        return 200  # Interval of 20 seconds
    else:
        return 220  # Interval of 30 seconds for larger files



class GetOrCreateThumbnailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        video_path = os.path.join(settings.MEDIA_ROOT, video.file_path)
        thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails', str(video_id))
        os.makedirs(thumbnail_dir, exist_ok=True)
        max_thumbnails = 12  # Maximum number of thumbnails

        # Check if thumbnails already exist
        thumbnails = [f for f in os.listdir(thumbnail_dir) if f.endswith('.jpg')]
        if len(thumbnails) == 0 and len(thumbnails) < max_thumbnails:
            # Determine the interval based on the video file size
            interval = get_thumbnail_interval(video.file_size)
            thumbnail_size = '360x240'  # Thumbnail resolution

            # Generate thumbnails with specific size
            command = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'select=not(mod(n\\,{interval * 10})),scale={thumbnail_size}',  # Adjust for fps and size
                '-vsync', 'vfr',
                '-q:v', '2',
                '-vframes', str(max_thumbnails),  # Limit to max_thumbnails frames
                os.path.join(thumbnail_dir, 'thumb%03d.jpg')
            ]
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Re-check for thumbnails after generation
            thumbnails = [f for f in os.listdir(thumbnail_dir) if f.endswith('.jpg')]

        # Truncate thumbnails if more than max_thumbnails
        if len(thumbnails) > max_thumbnails:
            thumbnails = thumbnails[:max_thumbnails]

        thumbnail_urls = [
            os.path.join('thumbnails', str(video_id), filename)
            for filename in thumbnails
        ]

        return Response(thumbnail_urls)

class ListTrimmedVideosView(generics.ListAPIView):
    serializer_class = TrimmedVideoSerializer

    def get_queryset(self):
        return TrimmedVideo.objects.filter(user=self.request.user).order_by('-pk')  

class TrimVideoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        if start_time is None or end_time is None:
            return Response({'error': 'Start time and end time are required'}, status=status.HTTP_400_BAD_REQUEST)

        video_path = os.path.join(settings.MEDIA_ROOT, video.file_path)
        trimmed_video_dir = os.path.join(settings.MEDIA_ROOT, 'trimmed_videos', str(video_id))
        os.makedirs(trimmed_video_dir, exist_ok=True)

        unique_id = str(uuid.uuid4())
        trimmed_video_filename = f'trimmed_{start_time}_{end_time}_{unique_id[:10]}.mp4'
        trimmed_video_path = os.path.join(trimmed_video_dir, trimmed_video_filename)

        command = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c', 'copy',
            trimmed_video_path
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get file size
        file_size = os.path.getsize(trimmed_video_path)

        # Save relative path
        relative_trimmed_video_path = os.path.relpath(trimmed_video_path, settings.MEDIA_ROOT)

        # Create a TrimmedVideo entry
        trimmed_video = TrimmedVideo.objects.create(
            user=request.user,
            original_video=video,
            file_path=relative_trimmed_video_path,
            file_size=file_size,
            start_time=start_time,
            end_time=end_time,
            name=trimmed_video_filename
        )

        # Return the URL to the trimmed video
        trimmed_video_url = os.path.join('trimmed_videos', str(video_id), trimmed_video_filename)

        return Response({'trimmed_video_url': trimmed_video_url}, status=status.HTTP_200_OK)


class MergedVideoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        merged_videos = MergedVideo.objects.filter(user=user)
        serializer = MergedVideoSerializer(merged_videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MergeTrimmedVideosView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        trimmed_video_ids = request.data.get('video_ids', [])
        name = request.data.get('name', 'Merged Video')

        if not trimmed_video_ids:
            return Response({'error': 'No trimmed videos selected'}, status=status.HTTP_400_BAD_REQUEST)

        trimmed_videos = TrimmedVideo.objects.filter(id__in=trimmed_video_ids)
        if not trimmed_videos.exists():
            return Response({'error': 'Some trimmed videos not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create a unique file path for the merged video
        unique_id = str(uuid.uuid4())
        merged_video_path = os.path.join(settings.MEDIA_ROOT, 'merged_videos', f'merged_{unique_id}.mp4')
        os.makedirs(os.path.dirname(merged_video_path), exist_ok=True)

        # Create a join_video.txt file with paths of videos to be merged
        join_file_path = os.path.join(settings.MEDIA_ROOT, 'merged_videos', 'join_video.txt')
        with open(join_file_path, 'w') as f:
            for video in trimmed_videos:
                f.write(f"file '{os.path.join(settings.MEDIA_ROOT, video.file_path)}'\n")

        # Build the ffmpeg command to merge videos using join_video.txt
        command = f'ffmpeg -f concat -safe 0 -i "{join_file_path}" -c copy "{merged_video_path}"'

        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            return Response({'error': f'Error merging videos: {e.stderr.decode()}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Clean up the join_video.txt file
            os.remove(join_file_path)

        # Get file size
        file_size = os.path.getsize(merged_video_path)

        # Create a MergedVideo entry
        merged_video = MergedVideo.objects.create(
            user=user,
            file_path=os.path.join('merged_videos', f'merged_{unique_id}.mp4'),
            file_size=file_size,
            name=name
        )
        merged_video.trimmed_videos.set(trimmed_videos)

        serializer = MergedVideoSerializer(merged_video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
