from django.db import models
from django.urls import reverse

from item.models import BaseTimestamp


class NotificationManager(models.Manager):
    """
    Override the Notification manager.
    """
    def notifications_received(self, receiver):
        """
        Take a receiver, and return all his received notifications.
        """
        qs = Notification.objects.filter(receiver=receiver).exclude(sender=receiver)
        return qs

    def notifications_count(self, receiver):
        """
        Take a receiver, and count his notifications.
        """
        qs_count = Notification.objects.filter(receiver=receiver, is_seen=False).exclude(sender=receiver).count()
        return qs_count    

    def notifications_updated(self, receiver):
        """
        Take a receiver, and update his notifications after seeing them.
        """
        qs = Notification.objects.filter(receiver=receiver, is_seen=False).update(is_seen=True)
        return qs

    def get_or_create_notification(self, sender, receiver, item, notification_type):
        """
        Take sender, receiver, item, and notification_type.
        Get the notification if it already exists, and if not, create a new notification.
        """
        # filter the queryset to check if the notification already exists or not. 
        qs_get = self.get_queryset().filter(sender=sender, receiver=receiver, item=item, notification_type=notification_type)
        # if the notification exists, get it.
        if qs_get.exists():
            return qs_get.first(), False
        # if not, create a new one.     
        return Notification.objects.create(sender=sender, receiver=receiver, item=item, notification_type=notification_type), True  
    
    def delete_notification(self, sender, item, notification_type):
        """
        Take sender, item, and notification_type.
        Delete the notification.
        """
        # get all tags of the item.
        item_tags = item.tags.all()
        # get a queryset of tag notifications excluding the ones of the item.
        qs_delete = self.get_queryset().filter(sender=sender, item=item, notification_type=notification_type).exclude(receiver__in=item_tags)
        if qs_delete.exists():
            for notify in qs_delete:
                # delete notification.
                notify.delete()    


class Notification(BaseTimestamp):
    """
    Notification model.
    """
    STATUS_CHOICES = (
        ('sent', 'sent'),
        ('accepted', 'accepted'),
    )

    NOTIFICATION_TYPE = (
        ('like', 'like'),
        ('comment', 'comment'),
        ('follow', 'follow'),
        ('tag', 'tag'),
        ('follow_request', 'follow request'),
        ('comment_like', 'comment like'),

    )

    sender = models.ForeignKey("profiles.UserProfile", on_delete=models.CASCADE, related_name='noti_from_user')
    receiver = models.ForeignKey("profiles.UserProfile", on_delete=models.CASCADE, related_name='noti_to_user')
    item = models.ForeignKey("item.Item", on_delete=models.CASCADE, related_name='noti_item', blank=True, null=True)
    comment = models.ForeignKey("item.Comment", on_delete=models.CASCADE, related_name='noti_comment', blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, blank=True, null=True)
    notification_type = models.CharField(max_length=14, choices=NOTIFICATION_TYPE)
    comment_snippt = models.CharField(max_length=90, blank=True, null=True)
    is_seen = models.BooleanField(default=False)
   
    objects = NotificationManager()
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        # Return sender's username, receiver's username, and the notification type.
        return f'{self.sender}-{self.receiver}-{self.notification_type}'

    def get_invitation_accept_absolute_url(self):
        # Return absolute url of follow request acceptance.
        return reverse('notifications:invitation-accept')

    def get_invitation_delete_absolute_url(self):
        # Return absolute url of follow request deletion.
        return reverse('notifications:invitation-delete')     

    