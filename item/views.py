from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from notifications.models import Notification
from explore.models import Hashtag
from profiles.models import UserProfile
from .models import Item, Comment
from .forms import ItemUpdateForm, CommentForm


@login_required
def item_detail_view(request, slug=None):
    """
    Take slug, get the item with this slug, and display the item detail.
    Create comment or reply to this item.
    """
    # get item by its slug
    item = get_object_or_404(Item, slug=slug)
    data = dict()
    # add comment
    form = CommentForm(request.POST or None)
    # check if the comment form is valid.
    if form.is_valid():
        # # Get data from the submitted form.
        content = request.POST.get('content')
        reply_id = request.POST.get('comment_id')
        reply = None
        # check if it's a comment or a reply to a comment.
        if reply_id:
            # get the id of the comment to add the reply to it.
            reply = Comment.objects.get(id=reply_id)
        # create comment for this item with requested user as an owner. 
        comment = Comment.objects.create(owner=request.user, item=item, reply=reply, content=content)
        # save comment.
        comment.save()
    context = {'item':item, 'comment_form':form}
    if request.is_ajax():
        data['comment_form'] = render_to_string('item/comments.html', context, request=request)
        data['partial_comment_list'] = render_to_string('item/partial_comment_list.html', context, request=request)
        data['comment_count'] = render_to_string('item/comment_count.html', context, request=request)
        return JsonResponse(data) 
    return render(request, 'item/item_detail.html', context)


@login_required
def item_upload_view(request):
    """
    Upload item view.
    """
    # get current user.
    user = request.user
    # check if the request method is post.
    if request.method == "POST":
        # Get data from the submitted data
        image = request.FILES.get('image')
        caption = request.POST.get('caption', None)
        hashtags = request.POST.get('hashtags', None)
        tags = request.POST.get('tags', None)
        restrict_comment = bool(request.POST.get('restrict_comment'))
        # create new item with the submitted data.
        new_item = Item.objects.create(owner=user, image=image, caption=caption, restrict_comment=restrict_comment)
        # if the submitted data has hashtags.  
        if hashtags:
            # convert the submitted hashtags string to a hashtags queryset.
            hashtags_qs = Hashtag.objects.hashtag_to_qs(hashtags)
            # add hashtags to the item's hashtags.
            new_item.hashtags.set(hashtags_qs)
        # if the submitted data has tags.     
        if tags:
            # convert the submitted tags string to a tags queryset.
            tags_qs = UserProfile.objects.tag_to_qs(tags)
            # add tags to the item's tags.
            new_item.tags.set(tags_qs) 
            # set the tag notification sender as the item's owner. 
            sender = new_item.owner.userprofile
            for tag in tags_qs:
                # set each tag as a notification receiver.
                receiver = tag
                # create tag notification for this item.
                Notification.objects.create(sender=sender, receiver=receiver, item=new_item, notification_type='tag')   
        return redirect('/') 
    return render(request, 'item/item_upload.html', {})             

@login_required
def item_update_view(request, slug=None):
    """
    Take slug, get the item with this slug, and update the item. 
    """
    # get item by its slug.
    item = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), slug=slug)
    # comment form
    comment_form = CommentForm()
    # get current item's hashtags
    hashtag_string = '#'
    hashtags_to_qs = " ".join(hashtag_string + x.name for x in item.hashtags.all())
    # get current item's hashtags
    tag_string = '@'
    tags_to_qs = " ".join(tag_string + x.user.username for x in item.tags.all())
    # update item  
    data = dict()
    # check if the request method is post.
    if request.method == 'POST':
        form = ItemUpdateForm(request.POST or None, instance=item, initial={'hashtags': hashtags_to_qs, 'tags':tags_to_qs})
        # if the form is valid.
        if form.is_valid():
            form.save()
            data['edit_item_form_is_valid'] = True
        # if not.
        else:
            data['edit_item_form_is_valid'] = False    
    # if not.
    else:
        form = ItemUpdateForm(instance=item, initial={'hashtags': hashtags_to_qs, 'tags':tags_to_qs})        
    context = {'item':item, 'item_update_form':form, 'comment_form':comment_form}
    data['html_data'] = render_to_string('item/item_update_form.html', context, request=request)
    data['comment_form'] = render_to_string('item/comments.html', context, request=request)
    data['item_caption'] = render_to_string('item/item_caption.html', context, request=request)
    data['item_tags_icon'] = render_to_string('item/item_tags.html', context, request=request)
    return JsonResponse(data) 

@login_required
def item_delete_view(request, slug=None):
    """
    Take slug, get the item with this slug, and delete the item.
    """
    # get item by its slug
    item = get_object_or_404(Item, slug=slug)
    # delete item
    data = dict()
    # check if the request method is post.
    if request.method == 'POST':
        # delete item.
        item.delete()
        return redirect('profiles:detail', username=request.user.username)
    context = {'item':item}    
    data['html_data'] = render_to_string('item/item_delete_form.html', context, request=request)
    return JsonResponse(data)

@login_required
def items_tags_view(request, slug=None):
    """
    Take slug, get the item with this slug, and display the item's tags.
    """
    # get item by its slug 
    item = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), slug=slug)
    # get item tags
    data = dict()
    tags_qs = item.tags.all()
    context = {'item': item, 'tags':tags_qs}
    data['html_data'] = render_to_string('item/tags.html', context, request=request)
    return JsonResponse(data) 

@login_required
def items_likes_display_view(request, slug=None):
    """
    Take slug, get the item with this slug, and display the item's likes.
    """
    # get item by its slug 
    item = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), slug=slug)
    # get item likes
    data = dict()
    likes_qs = item.likes.all()
    context = {'item': item, 'likes':likes_qs}
    data['html_data'] = render_to_string('item/item_likes.html', context, request=request)
    return JsonResponse(data) 

@login_required
def comment_likes_display_view(request, id=None):
    """
    Take id, get the comment with this id, and display the comment's likes.
    """
    # get comment by its id 
    comment = get_object_or_404(Comment.objects.select_related('owner', 'item', 'reply').prefetch_related('likes'), pk=id)
    # get comment likes
    data = dict()
    likes_qs = comment.likes.all()
    context = {'likes':likes_qs}
    data['html_data'] = render_to_string('item/comment_likes.html', context, request=request)
    return JsonResponse(data) 

@login_required
def comment_update_view(request, id=None):
    """
    Take id, get the comment with this id, and update the comment.
    """
    # get comment by its id.
    comment = get_object_or_404(Comment, pk=id)
    # get item of this comment.
    item = get_object_or_404(Item, pk=comment.item.id)
    # update comment
    data = dict()
    # check if the request method is post.
    if request.method == 'POST' and request.is_ajax():
        form = CommentForm(request.POST or None, instance=comment)
        # check if the comment form is valid.
        if form.is_valid():
            # save updated comment.
            form.save()
            data['edit_comment_form_is_valid'] = True
            data['partial_comment_list'] = render_to_string('item/partial_comment_list.html', {'item':item}, request=request) 
        else:
            data['edit_comment_form_is_valid'] = False 
        return JsonResponse(data)    
    else:
        form = CommentForm(instance=comment)           
        context = {'comment_update_form':form}
        data['html_data'] = render_to_string('item/comment_update_form.html', context, request=request)
        return JsonResponse(data) 

@login_required
def comment_delete_view(request, id=None):
    """
    Take id, get the comment with this id, and delete the comment.
    """
    # get comment by its id.
    comment = get_object_or_404(Comment, pk=id)
    # get item of this comment.
    item = get_object_or_404(Item, pk=comment.item.id)
    # delete comment
    data = dict()
    # check if the request method is post.
    if request.method == 'POST':
        # delete comment.
        comment.delete()
        data['delete_comment_form_is_valid'] = True
        context = {'item':item}
        data['partial_comment_list'] = render_to_string('item/partial_comment_list.html', context, request=request)
        data['comment_count'] = render_to_string('item/comment_count.html', context, request=request)        
    else:
        context = {'comment':comment}
        data['html_data'] = render_to_string('item/comment_delete_form.html', context, request=request)
    return JsonResponse(data)


# class ItemTagsAPIView(APIView):
#     """
#     """
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, format=None):
#         # Search by username.
#         query = request.GET.get('search')
#         profiles_qs = UserProfile.objects.filter(user__username__startswith=query)
#         profiles_lst = []  
#         profiles_lst += [i.user.username for i in profiles_qs]      
#         data = {
#             'profiles_lst': profiles_lst,
#         }
#         return Response(data)


class ItemLikeAPIToggle(APIView):
    """
    User Like Toggle View.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None, format=None):
        """
        Take slug, get item of this slug, and add or remove user to or from the item likes' list.
        Create like notification if user liked the item, and delete like notification if user unliked the item.  
        """
        # get item by its slug.
        item_obj = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), slug=slug)
        # get current user.
        user = request.user
        # set the notification sender as the requested user's profile.
        sender = user.userprofile
        # set the notification receiver as the item's owner. 
        receiver = item_obj.owner.userprofile
        updated = False
        liked = False
        # check if requested user is authenticated or not.
        if user.is_authenticated:
            # if the user has already liked this item.
            if user in item_obj.likes.all():
                liked = False
                # remove user from item's likes.
                item_obj.likes.remove(user)
                # get the like notification for this item with user as a sender, and profile as a receiver.
                notify = get_object_or_404(Notification, sender=sender, receiver=receiver, item=item_obj, notification_type='like')
                # delete like notification.
                notify.delete()
            # if not.    
            else:
                liked = True
                # add user to item's likes.
                item_obj.likes.add(user)
                # create a like notification for this item with user as a sender, and profile as a receiver.  
                Notification.objects.create(sender=sender, receiver=receiver, item=item_obj, notification_type='like') 
            updated = True
        # get likes count of this item.    
        likes_count = item_obj.likes.count()
        data = {
            'updated':updated,
            'liked':liked,
            'likes_count':likes_count,
        }           
        return Response(data)


class ItemFavouriteAPIToggle(APIView):
    """
    User Favourite Toggle View.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None, format=None):
        """
        Take a slug, get item of this slug, and add or remove user to or from the item favourites' list.
        """
        # get item by its slug.
        item_obj = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), slug=slug)
        # get current user.
        user = request.user
        updated = False
        saved = False
        # check if requested user is authenticated or not.
        if user.is_authenticated:
            # if the user has already added this item to his favourites.
            if user in item_obj.favourites.all():
                saved = False
                # remove user from item's favourites.
                item_obj.favourites.remove(user)
            # if not.    
            else:
                saved = True
                # add user to item's favourites.
                item_obj.favourites.add(user) 
            updated = True
        data = {'updated':updated, 'saved':saved}           
        return Response(data)


class ItemCommentCountAPI(APIView):
    """
    Item comment count view. 
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug=None, format=None):
        """
        """
        # get item by its slug.
        item_obj = get_object_or_404(Item, slug=slug)
        url_ = item_obj.get_absolute_url()
        # get current user.
        user = request.user
        comments_count = item_obj.comments.count()
        data = {'comments_count':comments_count}           
        return Response(data)


class CommentLikeAPIToggle(APIView):
    """
    User Comment Like Toggle View.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None, format=None):
        """
        Take id, get comment of this id, and add or remove user to or from the comment likes' list.
        Create like comment notification if user liked the comment,
        delete like comment notification if user unliked the comment.
        """
        # get comment by its id.
        comment_obj = get_object_or_404(Comment.objects.select_related('owner', 'item', 'reply').prefetch_related('likes'), pk=id)
        # get current user.
        user = request.user
        # set the notification sender as the requested user's profile.
        sender = user.userprofile
        # set the notification receiver as the comment's owner. 
        receiver = comment_obj.owner.userprofile
        # set the notification item as the item of this comment.
        item_obj = comment_obj.item
        updated = False
        liked = False
        # check if requested user is authenticated or not.
        if user.is_authenticated:
            # if the user has already liked this comment.
            if user in comment_obj.likes.all():
                liked = False
                # remove user from comment's likes. 
                comment_obj.likes.remove(user)
                # get the like comment notification for this comment with user as a sender, profile as a receiver, and comment's item as a item.
                notify = get_object_or_404(Notification, sender=sender, receiver=receiver, item=item_obj, comment=comment_obj, notification_type='comment_like')
                # delete like comment notification.
                notify.delete()
            # if not.
            else:
                liked = True
                # add user to comment's likes. 
                comment_obj.likes.add(user)
                # create like comment notification for this comment with user as a sender, profile as a receiver, and comment's item as a item.
                Notification.objects.create(sender=sender, receiver=receiver, item=item_obj, comment=comment_obj, notification_type='comment_like') 
            updated = True
        # get likes count of this comment.    
        comment_likes_count = comment_obj.likes.count()
        data = {
            'updated':updated,
            'liked':liked,
            'likes_count':comment_likes_count,
        }           
        return Response(data)