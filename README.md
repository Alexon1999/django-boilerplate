# Notification System

This document describes how to set up a Notification System using `django-notifications-hq` to send/retrieve notifications.

[https://pypi.org/project/django-notifications-hq/](https://pypi.org/project/django-notifications-hq/)

```python

To generate an notification anywhere in your code, simply import the notify signal and send it with your actor, recipient, and verb.

from notifications.signals import notify

notify.send(user, recipient=user, verb='you reached level 10', target=instance)

# behind the scenes, this is equivalent to:
Notification.objects.create(
    actor=user,
    recipient=user,
    verb='you reached level 10',
    target=instance,
)
```