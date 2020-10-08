from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    """Data about users"""

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


class TimeModel(models.Model):
    """Data about timed solves."""

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    time = models.IntegerField()
    dnf = models.BooleanField()
    penalty = models.BooleanField()
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.time)


class CheckUsername(models.Model):
    """Logs username check ups."""

    username = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class CheckEmail(models.Model):
    """Logs email check ups."""

    email = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
