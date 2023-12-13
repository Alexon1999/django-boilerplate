# Email service with Django, Celery, RabbitMQ and Redis

This document describes how to set up an e-mail service using Django, Celery, RabbitMQ and Redis. 

## Introduction

- Django** is a high-performance Python web framework that encourages rapid development and clean, pragmatic design.

- Celery** is an asynchronous task queue based on message distribution. It focuses on real-time processing, but also supports scheduling.  The primary use case for Celery is to offload work from the application thread to a worker thread in a distributed environment. Here's what Celery typically handles:

- Celery Beat** is a task scheduler for Celery that allows periodic tasks to be triggered.

- RabbitMQ** is an open source message broker that provides a robust platform for routing messages between processes and applications.

- Redis** is an in-memory database that can be used as a results backend for Celery.


## Workflow

![Send Email Workflow](./doc/assets/img/email.png)

Task Creation: Within your Django application, a task (such as sending an email) is defined and triggered. This could be in response to a user action, a scheduled event, or any other logic within your application.

Task Offloading: The Django application offloads this task to Celery. This is typically done by calling a function decorated as a Celery task, often using the .delay() method for asynchronous execution. For example, send_mail.delay(...).

Task Queuing: Celery, upon receiving the task, places it in a message queue. This is where RabbitMQ comes into play. RabbitMQ acts as the message broker, holding the task in a queue until a worker is available to process it.

Task Processing: Celery workers, which are separate processes (or even separate machines) constantly listening to the queues in RabbitMQ, pick up the task when they are ready. The worker then executes the task.

Result Storage: Once the task is executed, the result (if any) is stored in the result backend, which in this case is Redis. This step is optional and depends on whether the task produces a result that needs to be stored or further processed.

Completion: After the task is executed and the result is stored (if applicable), the process is complete. The application can then access the result from the Redis backend if needed.

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

See the `emails/` application

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