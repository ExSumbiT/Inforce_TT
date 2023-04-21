from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    is_restaurant = models.BooleanField(default=False)
