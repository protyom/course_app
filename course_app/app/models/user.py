# Django
from django.contrib.auth.models import AbstractUser
from django.db import models


from course_app.app.managers import OverrideUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    objects = OverrideUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []