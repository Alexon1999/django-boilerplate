# Scheduler

This document describes how to schedules periodic tasks using Django, Celery, RabbitMQ and Redis. 

## Introduction

- Django** is a high-performance Python web framework that encourages rapid development and clean, pragmatic design.

- Celery** is an asynchronous task queue based on message distribution. It focuses on real-time processing, but also supports scheduling.  The primary use case for Celery is to offload work from the application thread to a worker thread in a distributed environment. Here's what Celery typically handles:

- Celery Beat** is a task scheduler for Celery that allows periodic tasks to be triggered.

- RabbitMQ** is an open source message broker that provides a robust platform for routing messages between processes and applications.

- Redis** is an in-memory database that can be used as a results backend for Celery.

## Installation

Make sure you install the necessary dependencies:

```bash
pip install django celery django-celery-beat redis
```

For RabbitMQ, you can install it using your operating system's package managers. For example, for Ubuntu:

```bash
sudo apt-get install rabbitmq-server
```

## Configuration

### Django

Configure Django to use Celery and Redis as a results backend. Add these lines to your `settings.py` file:

```python
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
```

### Celery

Create a `celery.py` file in the same folder as your `settings.py` file with the following contents:

```python
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")

app = Celery("your_project_name")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

### Tasks

Define your tasks in a `tasks.py` file in one of your Django applications.
The file must be named `tasks.py` for celery to take it into account.

See example in emails/tasks.py


### Usage
for example in a Views : 
```python
send_mail.delay(...)
```

See the `scheduler/` application


### Scheduling

Use the `CrontabSchedule` template from `django-celery-beat` to define when a task should run. For example, to run a task every day at 9:00 am:

```python
from django_celery_beat.models import PeriodicTask, CrontabSchedule

schedule, _ = CrontabSchedule.objects.get_or_create(
    hour=9,
    minute=0,
)

PeriodicTask.objects.create(
    crontab=schedule,
    name="Send email every day at 9:00 AM",
    task="myapp.tasks.send_email",
    args=json.dumps(["Subject", "Message", "from@example.com", ["to@example.com"]]),
)
```

## Running

To run your e-mail service, you need to start the Django server, the Celery worker and the Celery Beat scheduler:

```bash
# Start the Django server
python manage.py runserver

# Start the Celery worker
celery -A your_project_name worker --loglevel=info

# Start Celery Beat scheduler
celery -A your_project_name beat --loglevel=info
```