from django.urls import path

from .views import index as views_index
from .views import test_send_email_views

app_name = "api"


urlpatterns = [
    path("index/", views_index.index, name="index"),
    path(
        "test-send-email/",
        test_send_email_views.TestSendEmailView.as_view(),
        name="test_send_email",
    ),
]
