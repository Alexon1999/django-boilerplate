from rest_framework import serializers


class CreateNotificationSerializer(serializers.Serializer):
    message = serializers.CharField()
