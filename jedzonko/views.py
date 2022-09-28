from datetime import datetime

from django.core import paginator

from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


def dashboard(request):
    return render(request, 'dashboard.html')
    

class RecipeDetailView(View):
    def get(self, request):
        return render(request, 'app-recipe-details.html')


class RecipesView(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by('votes').order_by('created')
        return render(request, 'app-recipes.html', {'recipes': recipes})


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

