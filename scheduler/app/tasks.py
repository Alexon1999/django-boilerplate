import logging

from celery import shared_task

from django.utils import timezone

logger = logging.getLogger("django")


@shared_task
def my_task():
    current_time = timezone.now()
    logger.info("launching task at %s", current_time)

    # do something
    # this could be task like updating status of an entity, sending a notification,
    # when a certain time has passed
    # or it could be a task that runs periodically
