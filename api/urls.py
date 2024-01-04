from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    index,
    EntityListApiView
)

app_name = "api"


urlpatterns = [
    path("index", index, name="index"),
    path(
        "entities/",
        cache_page(600,
                   key_prefix="cached_entities"
                   )(EntityListApiView.as_view()),
        name="cached_entities",
    ),
]
