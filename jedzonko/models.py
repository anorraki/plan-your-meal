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


# brownie = Recipe()
# brownie.name = "Brownie"
# brownie.ingredients = "Buraki gotowane, gorzka czekolada, jajka, migdały, mąka kokosowa, olej kokosowy, sól, proszek do pieczenia."
# brownie.description = "Dietetyczne brownie bez dodatku cukru, idealne do zielonej kawy z mlekiem z orzechów macadamia."
# brownie.preparation_time = 65
# brownie.votes = 10
# brownie.save()
#
# apple_pie = Recipe()
# apple_pie.name = "Apple Pie"
# apple_pie.ingredients = "Jabłka, gruszki, mąka pszenna, jajka, mleko, proszek do pieczenia, masło"
# apple_pie.description = "Pyszna, dietetyczna szarlotka bez cukru, najlepiej smakuje na ciepło z lodami waniliowymi i bitą śmietaną"
# apple_pie.preparation_time = 75
# apple_pie.votes = 9
# apple_pie.save()
#
# gofry = Recipe()
# gofry.name = "Goferki"
# gofry.ingredients = "Jajka, mąka migdałowa, mąka kokosowa, drożdże"
# gofry.description = "Pyszne i chrupiące goferki, najlepsze z bitą śmietaną, nutellą i owocami"
# gofry.preparation_time = 35
# gofry.votes = 8
# gofry.save()
#
# all = Recipe.objects.all()
# print(all)