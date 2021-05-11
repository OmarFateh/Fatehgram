import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from notifications.models import Notification 
from .models import UserProfile
from .forms import UserForm, ProfileForm


# Restrict the unauthenticated user from visiting this page and redirect to login page. 
@login_required 
def user_profile_detail(request, username):
    """
    Take username, get the profile with this username, and display the profile detail.
    """
    # get profile by its username. 
    profile = get_object_or_404(UserProfile, user__username=username)
    # get profile posts. 
    items_qs = profile.user.items.all() 
    # get profile saved posts.
    items_saved_qs = profile.user.favourites.all()
    # get profile tagged posts.
    items_tagged_qs = profile.tags.all()
    # check if the user is the owner of this profile to edit. 
    editable = False
    if request.user == profile.user:
        editable = True
    # check if the profile is private or not. 
    private_account = False
    if profile.private_account and request.user.userprofile not in profile.user.followers.all() and request.user != profile.user:
        private_account = True 
    # check if the user has already sent a follow request to this profile or not. 
    user = request.user.userprofile
    is_requested = UserProfile.objects.is_request_sent(user, profile)                   
    context = {
        'profile':profile, 
        'items':items_qs, 
        'saved_items':items_saved_qs, 
        'tagged_items':items_tagged_qs,
        'editable':editable, 
        'private_account':private_account,
        'is_requested':is_requested,
    }
    return render(request, 'profiles/profile_detail.html', context)

@login_required
def user_profile_update(request, username):
    """
    Take username, get the profile with this username, and update the profile.
    """
    # get profile by its username 
    profile = get_object_or_404(UserProfile, user__username=username)
    # get profile followers
    followers_qs = profile.get_follower.all()
    # get profile following
    following_qs = profile.following.all()
    # update profile
    data = dict()
    # check if the request method is post.
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=profile.user, request=request)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile) 
        # if the user form and profile form are valid.
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() 
            profile_form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        # display forms with current user profile data.
        user_form = UserForm(instance=profile.user, request=request)
        profile_form = ProfileForm(instance=profile)   
    context = {'profile':profile, 'followers':followers_qs, 'following':following_qs, 'user_form':user_form, 'profile_form':profile_form}
    data['html_data'] = render_to_string('profiles/includes/partial_profile_update_form.html', context, request=request)
    data['partial_profile_update'] = render_to_string('profiles/includes/partial_profile_update.html', context, request=request)
    return JsonResponse(data) 

@login_required
def profile_followers(request, username):
    """
    Take username, get the profile with this username, and display the profile's followers.
    """
    # get profile by its username 
    profile = get_object_or_404(UserProfile, user__username=username)    
    # get profile followers
    data = dict()
    followers_qs = profile.get_follower.all()
    context = {'profile': profile, 'followers':followers_qs,}
    data['html_data'] = render_to_string('profiles/includes/followers.html', context, request=request)
    return JsonResponse(data)

@login_required
def profile_following(request, username):
    """
    Take username, get the profile with this username, and display the profile's following.
    """
    # get profile by its username 
    profile = get_object_or_404(UserProfile, user__username=username)
    # get profile following
    data = dict()
    following_qs = profile.following.all()
    context = {'profile': profile, 'following':following_qs}
    data['html_data'] = render_to_string('profiles/includes/following.html', context, request=request)
    return JsonResponse(data)    

def search_profiles(request):
    """
    Search profiles by username, ordered alphabetically by username.
    """
    # get entered value in search input field.
    q = request.GET.get('search')
    data = dict()
    # filter profiles by username, ordered alphabetically by username.
    profiles_list_data = UserProfile.objects.get_profiles_list_data(q)
    return JsonResponse(json.dumps(profiles_list_data), content_type='application/json', safe=False)
   

class UserFollowAPIToggle(APIView):
    """
    User Follow Toggle View.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username=None, format=None):
        """
        Take username, get profile of this username, and send follow request, 
        add or remove user to or from the profile follower's list.
        Create follow notification if user followed the profile,
        delete follow notification if user unfollowd the profile,
        create follow request notification if profile is private.  
        """
        # get profile by its username.
        profile_obj = get_object_or_404(UserProfile, user__username=username)
        # check if the profile is private or not.
        private_account = False
        if profile_obj.private_account and request.user.userprofile not in profile_obj.user.followers.all() and request.user != profile_obj.user:
            private_account = True  
        user = request.user.userprofile
        updated = False
        followed_by = False
        sent_follow_request = False  
        # check if requested user is authenticated or not.
        if request.user.is_authenticated:
            # if the user is in profile's followers.
            if user in profile_obj.user.followers.all():
                followed_by = False
                # remove user from profile's followers.
                profile_obj.user.followers.remove(user)
                # get the follow notification with user as a sender, and profile as a receiver.
                notify = get_object_or_404(Notification, sender=user, receiver=profile_obj, notification_type='follow')
                # delete follow notification.
                notify.delete()
            # if profile is private account    
            elif private_account:
                sent_follow_request = True
                # check if the user has already sent a follow request to this profile or not. 
                is_requested = UserProfile.objects.is_request_sent(user, profile_obj) 
                if not is_requested:
                    # create a follow request notification of sent as a status type with user as a sender, and profile as a receiver.  
                    Notification.objects.create(sender=user, receiver=profile_obj, status='sent', notification_type='follow_request')
            # if the user is not in profile's followers and profile is not private account.
            else:
                followed_by = True
                # add user to profile's followers.
                profile_obj.user.followers.add(user) 
                # create a follow notification with user as a sender, and profile as a receiver. 
                Notification.objects.create(sender=user, receiver=profile_obj, notification_type='follow')
            updated = True
        data = {
            'updated':updated,
            'followed_by':followed_by,
            'sent_follow_request':sent_follow_request,
        }
        # get profile followers
        followers_qs = profile_obj.get_follower.all()
        # get profile following
        following_qs = profile_obj.following.all()
        # suggested profiles
        suggested_profiles = UserProfile.objects.suggested_profiles(user)[:6]
        context = {'profile':profile_obj, 'followers':followers_qs, 'following':following_qs, 'suggested_profiles':suggested_profiles}
        data['profile_navbar'] = render_to_string('profiles/includes/partial_profile_navbar.html', context, request=request)
        data['suggested_profiles'] = render_to_string('home/includes/suggested_profiles.html', context, request=request)
        return Response(data)