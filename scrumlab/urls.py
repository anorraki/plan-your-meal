"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko import views
from jedzonko.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('main/', views.DashboardView.as_view()),
    path('recipe/<int:recipe_id>/', views.RecipeDetailView.as_view()),
    path('recipe/list/', views.RecipesView.as_view(), name='receipes'),
    path('recipe/add/', views.AddRecipeView.as_view()),
    path('recipe/modify/<int:recipe_id>/', views.EditRecipeView.as_view()),
    path('recipe/delete/<int:recipe_id>/', views.DeleteRecipeView.as_view()),
    path('plan/list/', views.PlansView.as_view()),
    path('plan/<int:plan_id>/', views.PlanDetailView.as_view()),
    path('plan/add/', views.AddPlanView.as_view()),
    path('plan/delete/<int:plan_id>/', views.DeletePlanView.as_view()),
    path('plan/add-recipe/', views.AddRecipeToPlanView.as_view()),
    path('plan/delete-recipe/<int:plan_id>/<int:recipe_plan_id>/', views.DeleteRecipeFromPlanView.as_view()),

]
