from django.urls import path

from .views import index as views_index

app_name = "api"


urlpatterns = [
    path("index/", views_index.index, name="index"),
]
