from django.urls import path

from .views import (
        item_detail_view,
        item_upload_view, 
        item_update_view, 
        item_delete_view,
        items_tags_view,
        items_likes_display_view,
        comment_likes_display_view,
        comment_update_view,
        comment_delete_view,
        # ItemTagsAPIView,
        ItemLikeAPIToggle, 
        ItemFavouriteAPIToggle, 
        ItemCommentCountAPI,
        CommentLikeAPIToggle,
    )

urlpatterns = [
    # item
    path('p/<str:slug>/', item_detail_view, name='detail'),
    path('upload/', item_upload_view, name='upload'),
    path('p/<str:slug>/update/', item_update_view, name='update'),
    path('p/<str:slug>/delete/', item_delete_view, name='delete'),
    path('p/<str:slug>/likes/', items_likes_display_view, name='item-likes'),

    # comment
    path('c/<int:id>/update/', comment_update_view, name='comment-update'),
    path('c/<int:id>/delete/', comment_delete_view, name='comment-delete'),
    path('c/<int:id>/likes/', comment_likes_display_view, name='comment-likes'),

    # tags
    path('p/<str:slug>/tags/', items_tags_view, name='tags'),
    # path('ajax/autocomplete/tags', ItemTagsAPIView.as_view(), name='add-tags'), 

    # api ajax    
    path('api/<str:slug>/like/', ItemLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('api/<str:slug>/favourite/', ItemFavouriteAPIToggle.as_view(), name='favourite-api-toggle'),
    path('api/<str:slug>/comment_count/', ItemCommentCountAPI.as_view(), name='comment-api-count'),
    path('api/<int:id>/comment_like/', CommentLikeAPIToggle.as_view(), name='comment-api-like'),

]    