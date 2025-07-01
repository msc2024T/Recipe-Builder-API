from django.urls import path
from .views import RecipeView, RecipeDetailView, IngredientView, IngredientDetailView

urlpatterns = [
    path('recipe/', RecipeView.as_view(), name='recipe-list'),
    path('recipe/<int:recipe_id>/',
         RecipeDetailView.as_view(), name='recipe-detail'),
    path('ingredient/', IngredientView.as_view(), name='ingredient-list'),
    path('ingredient/<int:ingredient_id>/',
         IngredientDetailView.as_view(), name='ingredient-detail'),

]
