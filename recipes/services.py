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
