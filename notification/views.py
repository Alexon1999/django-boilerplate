from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from notifications.models import Notification
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from notification.filters import NotificationFilter

from .serializers import NotificationSerializer


@extend_schema_view(
    get=extend_schema(
        operation_id="ListNotification",
        summary="List Notification Read",
        description="List Notification Read",
    )
)
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = NotificationFilter

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user)


@extend_schema_view(
    put=extend_schema(
        operation_id="MarkNotificationRead",
        summary="Mark Notification as Read",
        description="Mark Notification as Read",
        request=None,
    )
)
class MarkNotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ["PUT"]

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.recipient != request.user:
            return Response(
                {"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN
            )
        notification.mark_as_read()
        return Response(
            {"detail": "Notification marked as read"}, status=status.HTTP_200_OK
        )


@extend_schema_view(
    put=extend_schema(
        operation_id="MarkAllNotificationRead",
        summary="Mark All Notification as Read",
        description="Mark All Notification as Read",
        request=None,
    )
)
class MarkAllNotificationsReadView(views.APIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        # Get all unread notifications for the user
        unread_notifications = Notification.objects.unread().filter(
            recipient=request.user
        )

        # Mark all of them as read
        unread_notifications.mark_all_as_read()

        return Response(
            {"detail": "All notifications marked as read."}, status=status.HTTP_200_OK
        )
