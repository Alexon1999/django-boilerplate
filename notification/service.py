from notifications.signals import notify


class NotificationService:
    @staticmethod
    def send_notification(
        sender, recipient, verb, description=None, action_object=None, target=None
    ):
        """
        Send a notification to a user.

        Args:
            sender (User instance): User instance sending the notification.
            recipient (User instance): User instance receiving the notification.
            verb (str): Verb describing the action.
            description (str, optional): Additional description. Defaults to None.
            action_object (Model instance, optional): The object triggering the action.
            target (Model instance, optional): The target object related to the action.
        """
        # The first element of the returned tuple is the created Notification instance(s)
        created_notifications = notify.send(
            sender=sender,
            recipient=recipient,
            verb=verb,
            description=description,
            action_object=action_object,
            target=target,
        )[0][1]

        # Get the first notification
        notification_instance = created_notifications[0]

        return notification_instance
