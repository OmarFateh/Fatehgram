from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from profiles.models import UserProfile
from .models import Notification


@login_required
def profile_notifications_view(request):
    """
    Display profile notifications.
    """
    # get profile of current user. 
    profile = get_object_or_404(UserProfile, user=request.user)    
    # get profile notifications.
    notifications = Notification.objects.notifications_received(profile)
    # update profile notifications from not seen to seen. 
    Notification.objects.notifications_updated(profile)
    context = {'profile': profile, 'notifications':notifications}
    return render(request, 'notifications/notifications.html', context)

@login_required
def invitation_accept_view(request):
    """
    Accept follow request.
    Change follow request notification to follow notification.
    """
    # get profile of current user 
    profile = get_object_or_404(UserProfile, user=request.user)
    # get profile notifications
    notifications = Notification.objects.notifications_received(profile)
    context = {'profile': profile, 'notifications':notifications}
    # accept invitation
    data = dict()
    # check if the request method is post.
    if request.method == 'POST':
        # Get data from the submitted data
        sender_pk = request.POST.get("profile_pk")
        # get sender's profile.
        sender = get_object_or_404(UserProfile, pk=sender_pk)
        # get receiver's profile, current user's profile.
        receiver = get_object_or_404(UserProfile, user=request.user)
        # get notification with submitted data.
        notify = get_object_or_404(Notification, sender=sender, receiver=receiver, notification_type='follow_request')
        # change notification status to accepted and notification type to follow, and save it.
        if notify.status == 'sent':
            notify.status = 'accepted'
            notify.notification_type = 'follow'
            notify.save()
            data['partial_notifications'] = render_to_string('notifications/includes/partial_notifications.html', context, request=request)          
        return JsonResponse(data)           

@login_required
def invitation_delete_view(request):
    """
    Delete follow request, and its notification.
    """
    # get profile of current user 
    profile = get_object_or_404(UserProfile, user=request.user)
    # get profile notifications
    notifications = Notification.objects.notifications_received(profile)
    context = {'profile': profile, 'notifications':notifications}
    # delete invitation
    data = dict()
    # check if the request method is post.
    if request.method == 'POST':
        # Get data from the submitted data
        sender_pk = request.POST.get("profile_pk")
        # get sender's profile.
        sender = get_object_or_404(UserProfile, pk=sender_pk)
        # get receiver's profile, current user's profile.
        receiver = get_object_or_404(UserProfile, user=request.user)
        # get notification with submitted data.
        notify = get_object_or_404(Notification, sender=sender, receiver=receiver, notification_type='follow_request')
        # delete notification.
        notify.delete()
        data['partial_notifications'] = render_to_string('notifications/includes/partial_notifications.html', context, request=request)          
        return JsonResponse(data)