# core/urls.py
from django.urls import path
from .views import VideoUploadView, UserVideoListView, GetOrCreateThumbnailsView, TrimVideoView

urlpatterns = [
    path('', VideoUploadView.as_view(), name='video-upload'),
    path('user/', UserVideoListView.as_view(), name='user-videos-list'),
    path('thumbnails/<int:video_id>/', GetOrCreateThumbnailsView.as_view(), name='get_or_create_thumbnails'),
    path('trim/<int:video_id>/', TrimVideoView.as_view(), name='trim-video'),
]
