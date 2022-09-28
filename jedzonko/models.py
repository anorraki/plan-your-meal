from django.db import models
from django.utils.datetime_safe import date


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now_add=False, default=date.today)
    updated = models.DateField(auto_now=False, default=date.today)
    preparation_time = models.IntegerField()
    votes = models.PositiveIntegerField(default=0)


