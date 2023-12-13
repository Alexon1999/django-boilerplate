from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from notification.service import NotificationService
from rest_framework.permissions import IsAuthenticated


class TestCreateNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        NotificationService.send_notification(
            sender=request.user,
            recipient=request.user,
            verb="test",
            description="This is a test notification",
        )
        return Response(status=status.HTTP_200_OK)
