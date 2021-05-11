from django.urls import path

from .views import (
    profile_notifications_view,
    invitation_accept_view,
    invitation_delete_view,
)    

urlpatterns = [
    # notification
    path('notifications/', profile_notifications_view, name='show-notifications'),

    # invitation
    path('i/accept/', invitation_accept_view, name='invitation-accept'),
    path('i/delete/', invitation_delete_view, name='invitation-delete'),
]