from django.urls import path

from .views import (
    MarkAllNotificationsReadView,
    MarkNotificationReadView,
    NotificationListView,
)

app_name = "notification"

urlpatterns = [
    path("list/", NotificationListView.as_view(), name="notification_list"),
    path(
        "list/<int:id>/read/",
        MarkNotificationReadView.as_view(),
        name="mark_notification_read",
    ),
    path(
        "list/read-all/",
        MarkAllNotificationsReadView.as_view(),
        name="mark_all_notification_read",
    ),
]
