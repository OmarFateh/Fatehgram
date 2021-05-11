from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item
from .models import Hashtag

def explore_view(request):
    """
    Display all item of other users whose profiles are not privat, and not in user's following list.
    """
    # explore items
    user = request.user.userprofile
    items = Item.objects.explore(user)
    context = {'items':items}
    return render(request, 'explore/explore.html', context)

def hashtag_view(request, hashtag_slug=None):
    """
    Take slug of hashtag, and display all items that have this hashtag.
    """
    # get hashtag by its slug.
    hashtag = get_object_or_404(Hashtag, slug=hashtag_slug)
    # get all items that have this hashtag.
    items = Item.objects.filter(hashtags=hashtag)
    context = {'hashtag':hashtag, 'items':items}
    return render(request, 'explore/hashtag.html', context)