from django import template
from django.template.defaultfilters import stringfilter

from notifications.models import Notification

register = template.Library()

@register.filter(is_safe=True)
def is_requested(sender, receiver):
        """
        Custom filter.
        Take a sender and a receiver and check if a follow request has been already sent by a sender to a receiver.
        """
        is_request_sent = Notification.objects.filter(sender=sender, receiver=receiver, status='sent', notification_type='follow_request').exists()
        return is_request_sent    