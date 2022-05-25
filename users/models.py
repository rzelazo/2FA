from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Class that extends default django User model by adding the phone_number field.
    """
    phone_number = models.CharField(max_length=12)
