import random
import re
from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import Recipe, Plan, DayName, RecipePlan

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

        last_plan = Plan.objects.order_by('-created')[0]

        recipe_plans = RecipePlan.objects.filter(plan=last_plan).order_by('order')
        days_in_plan = set(day.day_name for day in recipe_plans.order_by('day_name'))

        return render(request, 'dashboard.html', {"recipes_count": recipes_count,
                                                  'num': num,
                                                  'last_plan': last_plan,
                                                  'recipe_plans': recipe_plans,
                                                  'days_in_plan': days_in_plan})


class RecipeDetailView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)

        # Stworzona lista składników, by składniki były wyświetlane w oddzielnych wersach
        ingreditents_list = list(re.split("\n|; ", recipe.ingredients))
        return render(request, 'app-recipe-details.html', {'recipe': recipe,
                                                           'ingredients': ingreditents_list})

    def post(self, request, recipe_id):
        recipe_idx = request.POST.get('recipe_id')
        like = request.POST.get('like')
        if like == 'like':
            recipe = Recipe.objects.get(id=recipe_idx)
            recipe.votes += 1
            recipe.save()
            return redirect(f"/recipe/{recipe_id}")
        else:
            recipe = Recipe.objects.get(id=recipe_idx)
            recipe.votes -= 1
            recipe.save()
            return redirect(f'/recipe/{recipe_id}')


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
    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        day_name = DayName.objects.count()
        detail_dict = {}
        for day in range(1, day_name+1):
            query_set = plan.recipeplan_set.filter(day_name=day).order_by("order")
            if query_set.count() != 0:
                detail_dict[plan.recipeplan_set.filter(day_name=day)[0].day_name.day_name] = query_set[::1]
        return render(request, 'app-details-schedules.html', {'plan': plan,
                                                              'datail_dict': detail_dict})


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
        return redirect(f"/plan/{new_id}/")


class EditPlanView(View):
    def get(self, request):
        return render(request, 'app-edit-schedules.html')


class AddRecipeToPlanView(View):
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        return render(request, "app-schedules-meal-recipe.html", {'plans': plans, 'recipes': recipes, 'days': days})

    def post(self, request):
        plan_name = request.POST.get('choosePlan')
        meal_name = request.POST.get('mealName')
        order = request.POST.get('mealNumber')
        day = request.POST.get('day')
        recipe = request.POST.get('recipe')

        plan_instance = Plan.objects.get(name=plan_name)
        recipe_instance = Recipe.objects.get(name=recipe)
        day_instance = DayName.objects.get(day_name=day)
        recipe_instance_to_save = RecipePlan(
                meal_name=meal_name,
                recipe=recipe_instance,
                plan=plan_instance,
                order=order,
                day_name=day_instance)
        if plan_instance and meal_name and day_instance and recipe_instance and order:
            recipe_instance_to_save.save()
            chosen_plan = Plan.objects.get(name=plan_name).id
            message = messages.info(request, "Dodano przepis do planus")
            return redirect(f"/plan/{chosen_plan}/", {"message": message})
        else:
            message = messages.info(request, "Nie dodano przepisu do planu -- podaj wszystkie dane")
            return redirect("/plan/add-recipe/", {"message": message})

