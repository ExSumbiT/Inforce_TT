from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    is_restaurant = models.BooleanField(default=False)


class Restaurant(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    items = models.TextField()


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date = models.DateField()
