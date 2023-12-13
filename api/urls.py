from django.urls import path

from .views import index as views_index
from .views import test_create_notification_views

app_name = "api"


urlpatterns = [
    path("index", views_index.index, name="index"),
    path("test-create-notification/",
         test_create_notification_views.TestCreateNotificationView.as_view(
         ),
         name="test_create_notification"
         ),

]
