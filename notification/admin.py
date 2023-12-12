from django.contrib import admin

# Register your models here.
from notifications.models import Notification

#
# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
# list_display = ('recipient', 'actor', 'verb', 'target', 'action_object', 'timestamp')
# search_fields = ('recipient__username', 'actor__username', 'target__some_field')  # Add fields you want to search on
# list_filter = ('verb', 'timepythstamp')
