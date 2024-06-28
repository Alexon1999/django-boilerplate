import uuid

from django import utils
from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Departement(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Service(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    departement = models.ForeignKey(
        Departement, on_delete=models.CASCADE, related_name="departement"
    )
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Unite(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service"
    )
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    unite = models.ForeignKey(
        Unite, on_delete=models.SET_NULL, related_name="users", null=True, blank=True
    )
    birth_date = models.DateField(blank=True, null=True)
    company_start_date = models.DateField(blank=True, null=True)
    entity_start_date = models.DateField(blank=True, null=True)
    about = models.TextField()
    history = HistoricalRecords()


class TokenResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expiration_date = utils.timezone.now() + utils.timezone.timedelta(days=1)
        return super().save()

    @property
    def has_expired(self):
        return self.expiration_date < utils.timezone.now()


class ConfirmationEmailToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs) -> None:
        self.expiration_date = utils.timezone.now() + utils.timezone.timedelta(days=1)
        return super().save()
