from django.urls import path
from . import views


urlsAPI = [
    path('api/twitter',views.api_twitter, name='api_twitter'),
    # path('api/youtube',views.api_youtube, name='api_youtube'),
    # path('api/instagram',views.api_instagram, name='api_instagram'),
    # path('api/facebook',views.api_facebook, name='api_facebook'),    
]

urlsView = [
    path('test',views.test, name='test'),
    # path('twitter',views.twitter, name='twitter'),
    # path('youtube',views.youtube, name='youtube'),
    # path('instagram',views.instagram, name='instagram'),
    # path('facebook',views.facebook, name='facebook'),
]

urlpatterns = urlsAPI + urlsView