from django.urls import path
from .views import MealPlanView, MealPlanDetailView

urlpatterns = [
    path('meal-plans/', MealPlanView.as_view(), name='meal-plan-list'),
    path('meal-plans/<int:meal_plan_id>/',
         MealPlanDetailView.as_view(), name='meal-plan-detail'),
]
