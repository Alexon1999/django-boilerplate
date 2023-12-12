from django_filters import rest_framework as filters
from notifications.models import Notification


class NotificationFilter(filters.FilterSet):
    is_unread = filters.BooleanFilter(field_name='unread')
    # You can filter notifications by the verb, like 'liked', 'commented', etc.
    verb = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Notification
        fields = ['is_unread', 'verb']
