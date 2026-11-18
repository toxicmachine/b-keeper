from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MultipleObjectsReturned = None
    DoesNotExist = None
    email_notify = models.BooleanField(default=False, verbose_name='Уведомления на почту')