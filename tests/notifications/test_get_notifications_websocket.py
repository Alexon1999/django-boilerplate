import json
import pytest
from channels.testing import WebsocketCommunicator
from django.urls import reverse
from notifications.signals import notify
from rest_framework import status, test
from asgiref.sync import sync_to_async

from notification import consumers
from tests.data import factorys


def endpoint_login():
    return reverse("authentication:token-obtain-pair")


@pytest.fixture
def api_client():
    return test.APIClient()


@pytest.fixture
def test_data(db):
    user = factorys.UserFactory(username="test", is_active=True)
    user.set_password("password")
    user.save()

    user_enter = factorys.UserFactory()
    notify.send(user_enter, recipient=user, verb="new user in your unite")

    data_login = {
        "password": "password",
        "username": "test",
    }
    response_auth = test.APIClient().post(endpoint_login(), data=data_login)

    token = response_auth.data["access"]

    return {
        "user": user,
        "token": token,
    }


@pytest.mark.django_db
class TestValidationUser:
    def endpoint_login(self):
        return reverse("authentication:token-obtain-pair")

    @pytest.mark.asyncio
    @pytest.mark.django_db(transaction=True)
    async def test_get_notifications(self, api_client, test_data):
        user = test_data["user"]
        token = test_data["token"]

        api_client.force_authenticate(user)

        communicator = WebsocketCommunicator(
            consumers.NotificationCostumer.as_asgi(),
            path=f"ws://127.0.0.1:8000/websocket/?token={token}",
        )
        communicator.scope["user"] = user

        connected, _ = await communicator.connect()
        assert connected == True

        response = await communicator.receive_from()

        assert json.loads(response)["number_of_notifications"] == "1"
