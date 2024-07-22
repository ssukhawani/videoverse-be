# core/urls.py
from django.urls import path
from .views import VideoUploadView, UserVideoListView, GetOrCreateThumbnailsView, TrimVideoView, \
    ListTrimmedVideosView, MergedVideoListView, MergeTrimmedVideosView

urlpatterns = [
    path('', VideoUploadView.as_view(), name='video-upload'),
    path('user/', UserVideoListView.as_view(), name='user-videos-list'),
    path('thumbnails/<int:video_id>/', GetOrCreateThumbnailsView.as_view(), name='get_or_create_thumbnails'),
    path('trim/<int:video_id>/', TrimVideoView.as_view(), name='trim-video'),
    path('trimmed/', ListTrimmedVideosView.as_view(), name='list_trimmed_videos'),
    path('merged_videos/', MergedVideoListView.as_view(), name='merged_video_list'),
    path('merge_trimmed_videos/', MergeTrimmedVideosView.as_view(), name='merge_trimmed_videos'),
]
