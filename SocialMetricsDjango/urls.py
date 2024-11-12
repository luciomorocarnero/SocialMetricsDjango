from django.urls import path
from . import views


urlsAPI = [
    path('api/endpoints', views.endpoints, name='endpoints'),
    path('api/twitter',views.api_twitter, name='api_twitter'),
    path('api/youtube',views.api_youtube, name='api_youtube'),
    path('api/instagram',views.api_instagram, name='api_instagram'),
    # path('api/facebook',views.api_facebook, name='api_facebook'),
    path('api/tiktok',views.api_tiktok, name='api_tiktok'),    
]

urlsView = [
    path('test',views.test, name='test'),
    path('twitter',views.twitter, name='twitter'),
    path('youtube',views.youtube, name='youtube'),
    path('instagram',views.instagram, name='instagram'),
    path('tiktok',views.tiktok, name='tiktok'),
]

urlpatterns = urlsAPI + urlsView
