from notifications.signals import notify
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from notification.serializers import NotificationSerializer


class NotificationService:

    @staticmethod
    def send_notification(sender, recipient, verb, description=None, action_object=None, target=None):
        """
        Send a notification to a user.

        Args:
            sender (User instance): User instance sending the notification.
            recipient (User instance): User instance receiving the notification.
            verb (str): Verb describing the action.
            description (str, optional): Additional description. Defaults to None.
            action_object (Model instance, optional): The object triggering the action. Defaults to None.
            target (Model instance, optional): The target object related to the action. Defaults to None.
        """
        # The first element of the returned tuple will be the created Notification instance(s)
        created_notifications = notify.send(
            sender=sender,
            recipient=recipient,
            verb=verb,
            description=description,
            action_object=action_object,
            target=target
        )[0][1]

        # Get the first notification
        notification_instance = created_notifications[0]
        notification_instance_data = NotificationSerializer(
            notification_instance).data

        channel_layer = get_channel_layer()

        # Construct the group name based on recipient's ID
        group_name = f"notification_{recipient.id}"

        # Using the async_to_sync wrapper to call an async function from a synchronous context
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                # The name of the consumer method to call (see consumers.py)
                'type': 'notification.message',
                'data': notification_instance_data
            }
        )
