from django.urls import path
from .views import MealPlanView, MealPlanDetailView, MealPlanRecipeView

urlpatterns = [
    path('meal-plans/', MealPlanView.as_view(), name='meal-plan-list'),
    path('meal-plans/<int:meal_plan_id>/',
         MealPlanDetailView.as_view(), name='meal-plan-detail'),
    path('meal-plans/<int:meal_plan_id>/recipes/',
         MealPlanRecipeView.as_view(), name='meal-plan-recipe-list'),
]
