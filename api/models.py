from django.db import models
from authentication.models import User
# Create your models here.

class Entity(models.Model):

    STATUS_CHOICES = [
        ("submit", "submit"),
        ("waiting", "waiting"),
        ("new", "new"),
    ]

    status= models.CharField(max_length=10, choices=STATUS_CHOICES, default= "new")
    owner= models.ForeignKey(User, related_name="entities", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}{self.status}"
