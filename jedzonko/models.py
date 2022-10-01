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
    method = models.TextField()


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateField(auto_now_add=False, default=date.today)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')


class DayName(models.Model):
    day_name = models.CharField(max_length=16)
    order = models.IntegerField(unique=True)


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)

