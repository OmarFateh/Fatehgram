from django import forms

from explore.models import Hashtag
from profiles.models import UserProfile
from notifications.models import Notification
from .models import Item, Comment


class ItemUpdateForm(forms.ModelForm):
    """
    Item update model form
    """
    caption = forms.CharField(
        label='Caption',
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder':'Type something...'}),
    )
    hashtags = forms.CharField(
        label='Hashtags',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder':'Add hashtags... (add "#" before each hashtag)'}),
    )
    tags = forms.CharField(
        label="Friends' Tags",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder':'Tag friends...(add "@" before each username)'}), 
    )
    restrict_comment = forms.BooleanField(
        label='Restrict Comment',
        required=False,
        initial=False,
    )

    class Meta:
        model = Item 
        fields = ['caption', 'hashtags', 'tags', 'restrict_comment']

    def save(self, commit=True, *args, **kwargs):
        """
        Override the save method and add hashtags and tags to the item, before saving.
        """
        instance = super().save(commit=False, *args, **kwargs)
        # get data from the submitted data.
        hashtags = self.cleaned_data.get('hashtags')
        tags = self.cleaned_data.get('tags')
        if commit:
            # convert the submitted hashtags string to a hashtags queryset.
            hashtags_qs = Hashtag.objects.hashtag_to_qs(hashtags)
            # add hashtags to the item's hashtags.
            instance.hashtags.set(hashtags_qs)
            # convert the submitted tags string to a tags queryset.
            tags_qs = UserProfile.objects.tag_to_qs(tags)
            # add tags to the item's tags.
            instance.tags.set(tags_qs)
            # set the tag notification sender as the item's owner. 
            sender = instance.owner.userprofile
            # delete notifications of tags that are no longer exist.
            Notification.objects.delete_notification(sender=sender, item=instance, notification_type='tag')
            for tag in tags_qs:  
                # set each tag as a notification receiver.
                receiver = tag
                # get tag notification for this item if it already exists, if not, create new one.
                Notification.objects.get_or_create_notification(sender=sender, receiver=receiver, item=instance, notification_type='tag')
            if not instance.id:
                '''
                This is a new instance.
                '''
                instance.save()
            instance.hashtags.clear()
            instance.hashtags.add(*hashtags_qs)
            instance.tags.add(*tags_qs)
            instance.save()
        return instance
    

class CommentForm(forms.ModelForm):
    """
    Comment model form
    """
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class':'form-control input-sm', 'cols':'', 'rows':'', 'style': 'width: 89%; margin: 10px auto 0 15px;  resize:none;', 'placeholder':'Write your comment...'}))
    
    class Meta:
        model = Comment
        fields = ['content']