from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'actor_content_type', 'actor_object_id', 'verb', 'description',
                  'target_content_type', 'target_object_id', 'timestamp', 'unread')