import random
import re
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import Recipe, Plan, DayName, RecipePlan



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
            query_set = plan.recipeplan_set.filter(day_name=day)
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
        return redirect(f"/plan/{new_id}/details")


class EditPlanView(View):
    def get(self, request):
        return render(request, 'app-edit-schedules.html')


class AddRecipeToPlanView(View):
    def get(self, request):
        return render(request, 'app-schedules-meal-recipe.html')
