from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import CurrentUserView, MyTokenObtainPairView

app_name = "authentication"


urlpatterns = [
    path("api/token/", MyTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token-refresh"
    ),
    path("current-user/", CurrentUserView.as_view(), name="current-user"),
]
