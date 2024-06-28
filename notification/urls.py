from django.urls import path

from notification import views
from . import consumers

app_name = "notification"

urlpatterns = [
    path(
        "create-notification/",
        views.CreateNotificationView.as_view(),
        name="create_notification",
    ),
]

websocket_urls = [
    path("websocket/", consumers.NotificationCostumer.as_asgi()),
]
