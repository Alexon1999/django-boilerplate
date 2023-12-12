from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django_celery_beat.models import CrontabSchedule, PeriodicTask


@receiver(post_migrate)
def setup_periodic_tasks(sender, **kwargs):
    # Define the time (hour and minute) when you want the task to run
    # This will set the task to run every day at 6:00 AM
    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
        hour="6",
        minute="0",
        day_of_week="*",  # every day of the week
        day_of_month="*",  # every day of the month
        month_of_year="*",  # every month
    )

    periodic_task, _ = PeriodicTask.objects.get_or_create(
        crontab=crontab_schedule,
        name="Update assignment status every day at 6:00 AM",
        task="scheduler.app.tasks.update_assignments_status",
    )
