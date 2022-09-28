import random
from datetime import datetime
from django.shortcuts import render
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


def dashboard(request):
    return render(request, 'dashboard.html')
    

class RecipeDetailView(View):
    def get(self, request):
        return render(request, 'app-recipe-details.html')


class RecipesView(View):
    def get(self, request):
        return render(request, 'app-recipes.html')


class AddRecipeView(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')


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



