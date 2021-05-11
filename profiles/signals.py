from django.dispatch import receiver
from django.db.models.signals import post_save

from notifications.models import Notification

@receiver(post_save, sender=Notification)     # receiver(signal, **kwargs) # to register a signal
def add_to_following(sender, instance, created, **kwargs):
    """
    Add profile to following once the friend request is accepted.
    """
    sender_= instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.following.add(receiver_.user)
