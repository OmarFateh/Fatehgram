from django.urls import path

from .views import (
    user_profile_detail, 
    user_profile_update, 
    profile_followers, 
    profile_following, 
    search_profiles,
    UserFollowAPIToggle,
)    

urlpatterns = [
    # profile
    path('<str:username>/', user_profile_detail, name='detail'),
    path('<str:username>/edit/', user_profile_update, name='update'),
    path('<str:username>/followers/', profile_followers, name='followers'),
    path('<str:username>/following/', profile_following, name='following'),

    # search 
    path('ajax/profiles/search/', search_profiles, name='search'),

    # follow api toggle
    path('api/<str:username>/follow/', UserFollowAPIToggle.as_view(), name='follow-api-toggle'),
]    