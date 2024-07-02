import pytest

from authentication import models
from rest_framework import status, test
from rest_framework_simplejwt import tokens

from django.urls import reverse
from tests.auth.factorys import user_factory, confirmation_email_token_factory


@pytest.fixture
def test_data(db):
    user = user_factory.UserFactory(is_active=False)
    token = confirmation_email_token_factory.ConfirmationEmailTokenFactory(user=user)

    user_activate = user_factory.UserFactory(is_active=True)
    token_activate = confirmation_email_token_factory.ConfirmationEmailTokenFactory(
        user=user_activate
    )

    return {
        "user": user,
        "token": token,
        "user_activate": user_activate,
        "token_activate": token_activate,
    }


@pytest.fixture
def api_client():
    return test.APIClient()


@pytest.mark.django_db
class TestValidationUser:
    def endpoint(self, token):
        return reverse(
            "authentication:confirmation-activation-user", kwargs={"token": token}
        )

    def test_activation_user(self, api_client, test_data):
        user = test_data["user"]
        token = test_data["token"]

        response = api_client.get(self.endpoint(token.token))

        assert response.status_code == status.HTTP_200_OK

        access_response_token = tokens.AccessToken(response.data["access"])
        assert user.id == access_response_token["user_id"]

    def test_activate_already_activate_user(self, api_client, test_data):
        user_activate = test_data["user_activate"]
        token_activate = test_data["token_activate"]

        response = api_client.get(self.endpoint(token_activate.token))

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert (
            models.ConfirmationEmailToken.objects.filter(user=user_activate).count()
            == 0
        )
