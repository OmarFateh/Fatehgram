from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Item
from .utils import unique_slug_generator

@receiver(pre_save, sender=Item)     # receiver(signal, **kwargs) # to register a signal
def create_item_slug(sender, instance, *args, **kwargs):
    """
    Create a slug for an item before saving.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)