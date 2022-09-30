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


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateField(auto_now_add=False, default=date.today)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')


class DayName(models.Model):
    day_name = models.CharField(max_length=16)
    order = models.IntegerField().unique


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)

# r1 = Recipe()
# r1.name = "Spaghetti z boczniakami"
# r1.description = "Pyszne, pożywne dane z boczniakami, które na diecie wegetariańskiej są niesamowitym źródłem ultra potrzebnego białka."
# r1.preparation_time = 30
# r1.votes = 10
# r1.ingredients = "Parmezan, boczniaki, makaron, pomidory"
# r1.save()
#
# r2 = Recipe()
# r2.name = "Shake proteinowy"
# r2.description = "Shake proteinowy z białka sojowego, smak waty w jednym łyku"
# r2.ingredients = "Mleko migdałowe, białko wegetariańskie"
# r2.preparation_time = 5
# r2.votes = 4
# r2.save()
#
# r3 = Recipe()
# r3.name = "Curry z ciecierzycy"
# r3.ingredients = "Ciecierzyca, cukinia, pomidory, ryż basmati, oliwa, przyprawa curry"
# r3.description = "Sycące curry z ciecierzycy to idealny obiad na przepyszną kolację lub obiad w pracy."
# r3.preparation_time = 75
# r3.votes = 10
# r3.save()
#
# r4 = Recipe()
# r4.name = "Cukinia z kaszą jaglaną"
# r4.description = "Przepyszna cukinia pieczona, najlepiej smakuje do mięsa wołowego, ale jak jesteś wege to musisz obejść się smakiem"
# r4.ingredients = "Cukinia, parmezan, kasza jaglana, marchew, pomidory, oliwa"
# r4.preparation_time = 35
# r4.votes = 10
# r4.save()
#
#
# monday = DayName()
# monday.day_name = "Monday"
# monday.order = 1
#
# tuesday = DayName()
# tuesday.day_name = "Tuesday"
# tuesday.order = 2
#
# wednesday = DayName()
# wednesday.day_name = "Wednesday"
# wednesday.order = 3
#
# thursday = DayName()
# thursday.day_name = "Thursday"
# thursday.order = 4
#
# friday = DayName()
# friday.day_name = "Friday"
# friday.order = 5
#
# saturday = DayName()
# saturday.day_name = "Saturday"
# saturday.order = 6
#
# sunday = DayName()
# sunday.day_name = "Sunday"
# sunday.order = 7

# wege = Plan()
# wege.name = "Wege"
# wege.description = "Kupa błonnika, zero smaku, smutek w pierszym kęsie, depresja w gratisie"
#
# wege_plan = RecipePlan()
# wege_plan.meal_name = "Breakfast"
# wege_plan.recipe = r1
# wege_plan = wege
# wege_plan = 1

# gaca = Plan()
# gaca.name = "Karkówka oraz pomidory czyli jak schudnąć 20kg, nabawić się chorób, znienawidzić karkówkę i zrujnować swoje zdrowie"
# gaca.description = "Bardzo restrykcyjna i głupia dieta polegająca na eliminacji węglowodanów, jedzeniu tłustego mięsa jakim jest karkóweczka, zagryzanie to pomidorami, a po roku zastanawianie się czemu wyniki badań są tak złe. dzień dobry"
