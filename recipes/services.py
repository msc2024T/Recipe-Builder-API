from .models import Recipe, Ingredient, RecipeIngredient
from django.contrib.auth.models import User as AuthUser


class RecipeService:
    def create_recipe(self, title, instructions, image_path=None, created_by=None):
        if not title or not instructions:
            raise ValueError("Title and instructions are required")

        if created_by is None or not isinstance(created_by, AuthUser):
            raise ValueError("A valid user must be provided")

        # check if recipe with the same title already exists
        if Recipe.objects.filter(title=title, is_deleted=False).exists():
            raise ValueError("A recipe with this title already exists")

        recipe = Recipe(
            title=title,
            instructions=instructions,
            image_path=image_path,
            created_by=created_by
        )
        recipe.save()
        return recipe

    def get_recipe_list(self):
        return Recipe.objects.filter(is_deleted=False).order_by('-created_at')

    def get_recipe_by_id(self, recipe_id):
        try:
            return Recipe.objects.get(id=recipe_id, is_deleted=False)
        except Recipe.DoesNotExist:
            raise ValueError("Recipe not found")

    def delete_recipe(self, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id, is_deleted=False)
            recipe.is_deleted = True
            recipe.save()
            return True
        except Recipe.DoesNotExist:
            raise ValueError("Recipe not found")

    def update_recipe(self, recipe_id, title, instructions, image_path=None):
        try:
            recipe = Recipe.objects.get(id=recipe_id, is_deleted=False)
            recipe.title = title
            recipe.instructions = instructions
            recipe.image_path = image_path
            recipe.save()
            return recipe
        except Recipe.DoesNotExist:
            raise ValueError("Recipe not found")


class IngredientService:
    def create_ingredient(self, name, unit, image_path=None, created_by=None):
        if not name or not unit:
            raise ValueError("Name and unit are required")

        if created_by is None or not isinstance(created_by, AuthUser):
            raise ValueError("A valid user must be provided")

        # check if ingredient with the same name already exists
        if Ingredient.objects.filter(name=name, unit=unit, is_deleted=False).exists():
            raise ValueError(
                "An ingredient with this name and unit already exists")

        ingredient = Ingredient(
            name=name,
            unit=unit,
            image_path=image_path,
            created_by=created_by
        )
        ingredient.save()
        return ingredient

    def get_ingredient_list(self):
        return Ingredient.objects.filter(is_deleted=False).order_by('-created_at')

    def get_ingredient_by_id(self, ingredient_id):
        try:
            return Ingredient.objects.get(id=ingredient_id, is_deleted=False)
        except Ingredient.DoesNotExist:
            raise ValueError("Ingredient not found")

    def delete_ingredient(self, ingredient_id):
        try:
            ingredient = Ingredient.objects.get(
                id=ingredient_id, is_deleted=False)
            ingredient.is_deleted = True
            ingredient.save()
            return True
        except Ingredient.DoesNotExist:
            raise ValueError("Ingredient not found")

    def update_ingredient(self, ingredient_id, name, unit, image_path=None):
        try:
            ingredient = Ingredient.objects.get(
                id=ingredient_id, is_deleted=False)
            ingredient.name = name
            ingredient.unit = unit
            ingredient.image_path = image_path
            ingredient.save()
            return ingredient
        except Ingredient.DoesNotExist:
            raise ValueError("Ingredient not found")
