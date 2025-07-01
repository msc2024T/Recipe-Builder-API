from django.urls import path
from .views import RecipeView, RecipeDetailView

urlpatterns = [
    path('recipe/', RecipeView.as_view(), name='recipe-list'),
    path('recipe/<int:recipe_id>/',
         RecipeDetailView.as_view(), name='recipe-detail'),
]
