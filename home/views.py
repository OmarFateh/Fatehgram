from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from item.models import Item
from profiles.models import UserProfile


@login_required
def feed_view(request):
    """
    Display items of user and his following.
    Display trending items, items with most likes.
    Display suggested profile to follow.
    """
    # feed items
    user = request.user.userprofile
    items = Item.objects.feed(user)
    
    # trending items 
    trending_items = Item.objects.trending(user)[:6]

    # suggested profiles
    suggested_profiles = UserProfile.objects.suggested_profiles(user)[:6]
    context = {'items':items, 'trending_items':trending_items, 'suggested_profiles':suggested_profiles}
    return render(request, 'home/feed.html', context)