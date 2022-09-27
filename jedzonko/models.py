from django.db import models
from django.db.models import BigAutoField
from django.db.models.functions import datetime
from django.utils import timezone
from django.utils.datetime_safe import date


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now_add=False, default=date.today)
    updated = models.DateField(auto_now=False, default=date.today)
    preparation_time = models.IntegerField()
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Nazwa:{self.name}, Składniki:{self.ingredients}, Opis:{self.description}, Utworzono:{self.created},' \
               f'Zmodyfikowano:{self.updated}, czas przygotowania: {self.preparation_time} Oceny: {self.votes}.'


