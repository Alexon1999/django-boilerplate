from emails.tasks import send_mail
from emails.templating import TemplateEmailEnum

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TestSendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        send_mail.delay(
            to=["test@example.com"],
            subject="Test Email",
            template=TemplateEmailEnum.NEW_POST,
            context={
                "name": "John Doe",
            },
        )
        return Response("success", status=status.HTTP_200_OK)
