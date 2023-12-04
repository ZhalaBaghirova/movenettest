from django.urls import path
from .views import pose_estimation, video_feed
urlpatterns = [
    path('', pose_estimation, name='root_redirect'),
    path('pose_estimation/', pose_estimation, name='pose_estimation'),
    path('video_feed/', video_feed, name='video_feed'),
    # other URL patterns...
]
