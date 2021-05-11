from django.urls import path

from .views import explore_view, hashtag_view

urlpatterns = [
    # explore 
    path('explore/', explore_view, name='explore'),

    # hashtag
    path('explore/tags/<str:hashtag_slug>/', hashtag_view, name='hashtag'),
]    