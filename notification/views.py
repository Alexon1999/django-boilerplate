from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics, response, status

from notification import serializers as notification_serialziers


class CreateNotificationView(generics.CreateAPIView):
    serializer_class = notification_serialziers.CreateNotificationSerializer

    def create(self, request, *args, **kwargs):
        channel = get_channel_layer()

        async_to_sync(channel.group_send)(
            "notifications_new_user",
            {
                "type": "number_of_notifications",
            },
        )

        return response.Response(
            status=status.HTTP_201_CREATED,
            data=request.data["message"],
        )
