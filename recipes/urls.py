from django.urls import path
from .views import RecipeView, RecipeDetailView, IngredientView, IngredientDetailView, RecipeIngredientView, AddSingleRecipeIngredientView

urlpatterns = [
    path('recipe/', RecipeView.as_view(), name='recipe-list'),
    path('recipe/<int:recipe_id>/',
         RecipeDetailView.as_view(), name='recipe-detail'),
    path('ingredient/', IngredientView.as_view(), name='ingredient-list'),
    path('ingredient/<int:ingredient_id>/',
         IngredientDetailView.as_view(), name='ingredient-detail'),
    path('recipe/<int:recipe_id>/ingredient/',
         RecipeIngredientView.as_view(), name='recipe-ingredient-list'),
    path('recipe/<int:recipe_id>/ingredient/add/',
         AddSingleRecipeIngredientView.as_view(), name='add-recipe-ingredient'),

]
