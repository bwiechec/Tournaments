from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class UserUser(AbstractUser):
    birth_date = models.DateField('date birth', default=None, blank=True, null=True)
    email = models.EmailField('email address', unique=True, default=None, blank=True, null=True)

    objects = CustomUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.username)

    def __repr__(self):
        return repr(self.map)
