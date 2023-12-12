import importlib

from authentication.models import User

from notifications.models import Notification


def get_system_user():
    system_user, _ = User.objects.get_or_create(username="system")
    return system_user


def call_function(function_path, *args, **kwargs):
    module_path, function_name = function_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    function = getattr(module, function_name)
    function(*args, **kwargs)


def set_emailed(notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.emailed = True
    notification.save()
