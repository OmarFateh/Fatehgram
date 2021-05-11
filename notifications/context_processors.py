from django.shortcuts import get_object_or_404

from profiles.models import UserProfile
from notifications.models import Notification

def notifications_count(request):
    """
    Custom context processor for notifications count.
    """
    count_notifications = 0
    # check if current user is authenticated or not.
    if request.user.is_authenticated:
        # get profile of current user 
        profile = get_object_or_404(UserProfile, user=request.user)
        # get profile notifications count
        count_notifications = Notification.objects.notifications_count(profile)
    return {'count_notifications':count_notifications}     