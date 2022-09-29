import random
from datetime import datetime

from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import Recipe


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
        return render(request, 'dashboard.html', {"recipes_count": recipes_count})
    

class RecipeDetailView(View):
    def get(self, request):
        return render(request, 'app-recipe-details.html')


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
        if not name.strip(' ') or not ingredients.strip(' ') or \
                not description.strip(' ') or not preparation_time:
            return render(request, 'app-add-recipe.html', {'alert': 'Wypełnij poprawnie wszystkie pola.'})
        else:
            recipe = Recipe(name=name, ingredients=ingredients,
                        description=description, preparation_time=preparation_time)
            recipe.save()
            return redirect('/recipe/list/')


class EditRecipeView(View):
    def get(self, request):
        return render(request, 'app-edit-recipe.html')


class PlansView(View):
    def get(self, request):
        return render(request, 'app-schedules.html')


class PlanDetailView(View):
    def get(self, request):
        return render(request, 'app-details-schedules.html')


class AddPlanView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')


class EditPlanView(View):
    def get(self, request):
        return render(request, 'app-edit-schedules.html')


class AddRecipeToPlanView(View):
    def get(self, request):
        return render(request, 'app-schedules-meal-recipe.html')
