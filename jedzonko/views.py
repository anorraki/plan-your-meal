import random
import re
from datetime import datetime

from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import Recipe, Plan, RecipePlan, DayName


class IndexView(View):

    def get(self, request):
        all_recipes = list(Recipe.objects.all())
        random.shuffle(all_recipes)
        mixed_recipes = all_recipes[0:3]
        m1 = mixed_recipes[0]
        m2 = mixed_recipes[1]
        m3 = mixed_recipes[2]
        ctx = {"actual_date": datetime.now(),
               'm1': m1,
               'm2': m2,
               'm3': m3
               }
        return render(request, "index.html", ctx)


class DashboardView(View):

    def get(sefl, request):
        recipes_count = Recipe.objects.count()
        num = Plan.objects.count()
        return render(request, 'dashboard.html', {"recipes_count": recipes_count, 'num': num})


class RecipeDetailView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)

        # Stworzona lista składników, by składniki były wyświetlane w oddzielnych wersach
        ingreditents_list = list(re.split("\n|; ", recipe.ingredients))
        return render(request, 'app-recipe-details.html', {'recipe': recipe,
                                                           'ingredients': ingreditents_list})


class RecipesView(View):
    def get(self, request):
        recipes_lists = Recipe.objects.all().order_by('votes').order_by('-created')
        paginator = Paginator(recipes_lists, 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {'recipes': recipes})


class AddRecipeView(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        name = request.POST['recipe_name']
        ingredients = request.POST['recipe_ingredients']
        description = request.POST['recipe_description']
        preparation_time = request.POST['recipe_preparation']
        method = request.POST['recipe_method']
        if not name.strip(' ') or not ingredients.strip(' ') \
                or not description.strip(' ') or not preparation_time\
                or not method.strip(' '):
            return render(request, 'app-add-recipe.html', {'alert': 'Wypełnij poprawnie wszystkie pola.'})
        else:
            recipe = Recipe(name=name, ingredients=ingredients,
                            description=description, preparation_time=preparation_time,
                            method=method)
            recipe.save()
            return redirect('/recipe/list/')


class EditRecipeView(View):
    def get(self, request):
        return render(request, 'app-edit-recipe.html')


class PlansView(View):
    def get(self, request):
        plans = Plan.objects.all().order_by('name')
        paginator = Paginator(plans, 50)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        num = Plan.objects.count()
        return render(request, 'app-schedules.html', {'plans': plans, 'num': num})


class PlanDetailView(View):
    def get(self, request):
        return render(request, 'app-details-schedules.html')


class AddPlanView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        name = request.POST.get('planName')
        description = request.POST.get('planDescription')
        if name == '' or description == '':
            return render(request, 'app-add-schedules.html', {'error': "Proszę wpisać właściwe dane"})
        Plan(name=name, description=description).save()
        new_id = Plan.objects.get(name=name).id
        return redirect(f"/plan/{new_id}/details")


class EditPlanView(View):
    def get(self, request):
        return render(request, 'app-edit-schedules.html')


class AddRecipeToPlanView(View):
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        return render(request, "app-schedules-meal-recipe.html", {'plans': plans, 'recipes': recipes})

    def post(self, request):
        plan_name = request.POST.get('choosePlan')
        meal_name = request.POST.get('mealName')
        meal_number = request.POST.get('mealNumber')
        recipe = request.POST.get('recipe')
        day = request.POST.get('day')

        plan_instance = Plan.objects.get(name=plan_name)
        recipe_instance = Recipe.objects.get(name=recipe)
        day_instance = DayName.objects.get(day_name=day, order=True)

        RecipePlan.objects.create(meal_name=meal_name, recipe=recipe_instance, plan=plan_instance, order=meal_number, day_name=day_instance)
        chosen_plan = Plan.objects.filter(name=plan_name)
        plan_id = chosen_plan.id
        return redirect("/plan/"+plan_id+"/",)
        # return render(request, "app-schedules-meal-recipe.html", {'info': f'plan_name {plan_name}, meal_name {meal_name}, meal_number {meal_number}, recipe {recipe}, day {day}.'})
