# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from notifications.models import Notification
from api.models import Entity

@receiver(post_save, sender=Entity)
def entity_status_change(sender, instance, **kwargs):
    if instance.status == 'submit':
        print('here')
        print('instance.owner ', instance.owner)
        # Notify the owner when the status becomes 'submit'
        Notification.objects.create(
            actor=instance.owner,
            recipient=instance.owner,
            verb='Entity status changed to submit',
            target=instance,
        )