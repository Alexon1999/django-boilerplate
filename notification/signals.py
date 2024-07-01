from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from notifications.signals import notify

from authentication import models as auth_models
from notification import tasks, models


@receiver(post_save, sender=auth_models.User)
def notification_new_user_unit(sender, **kwargs):
    if kwargs['update_fields']:
        fields_name, = kwargs['update_fields']

        if fields_name == "unite":
            channel_layer = get_channel_layer()
            instance = kwargs['instance']
            query_user = auth_models.User.objects.filter(
                unite=instance.unite
            )

            notify.send(
                instance, recipient=query_user, verb="new user in your unite",
            )

            for user in query_user:
                number_of_notifications = user.notifications.unread().count()

                data = {
                    "type": "notifications.number",
                    "number": number_of_notifications,
                    "channel": user.username,
                }

                async_to_sync(channel_layer.group_send)(
                    f"notifications_{user.username}",
                    {
                        "type": "notifications.number",
                        "number_of_notifications": user.notifications.unread().count()
                    }
                )
