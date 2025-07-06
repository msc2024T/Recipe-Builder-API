from .models import Recipe, Ingredient, RecipeIngredient
from django.contrib.auth.models import User as AuthUser
from images.services import ImageService


class RecipeService:
    def create_recipe(self, title, instructions, image_id=None, created_by=None):
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
            image_id=image_id,
            created_by=created_by
        )
        recipe.save()

        image_service = ImageService(created_by)
        image_url = image_service.get_image_url(image_id) if image_id else None

        recipe.image_url = image_url
        return recipe

    def get_recipe_list(self):

        list = Recipe.objects.filter(is_deleted=False).order_by('-created_at')
        for recipe in list:
            image_service = ImageService(recipe.created_by)
            recipe.image_url = image_service.get_image_url(
                recipe.image_id) if recipe.image_id else None

        return list

    def get_recipe_by_id(self, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id, is_deleted=False)
            image_service = ImageService(recipe.created_by)
            recipe.image_url = image_service.get_image_url(
                recipe.image_id) if recipe.image_id else None
            return recipe

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

    def update_recipe(self, recipe_id, title, instructions, image_id=None):
        try:
            recipe = Recipe.objects.get(id=recipe_id, is_deleted=False)
            recipe.title = title
            recipe.instructions = instructions
            recipe.image_id = image_id
            image_service = ImageService(recipe.created_by)
            recipe.image_url = image_service.get_image_url(
                image_id) if image_id else None
            recipe.save()
            return recipe
        except Recipe.DoesNotExist:
            raise ValueError("Recipe not found")


class IngredientService:
    def create_ingredient(self, name, unit, image_id=None, created_by=None):
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
            image_id=image_id,
            created_by=created_by
        )
        ingredient.save()

        image_service = ImageService(created_by)
        image_url = image_service.get_image_url(image_id) if image_id else None

        ingredient.image_url = image_url

        return ingredient

    def get_ingredient_list(self):

        list = Ingredient.objects.filter(
            is_deleted=False).order_by('-created_at')
        for ingredient in list:
            image_service = ImageService(ingredient.created_by)
            ingredient.image_url = image_service.get_image_url(
                ingredient.image_id) if ingredient.image_id else None
        return list

    def get_ingredient_by_id(self, ingredient_id):
        try:
            ingredient = Ingredient.objects.get(
                id=ingredient_id, is_deleted=False)
            image_service = ImageService(ingredient.created_by)
            ingredient.image_url = image_service.get_image_url(
                ingredient.image_id) if ingredient.image_id else None

            return ingredient

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

    def update_ingredient(self, ingredient_id, name, unit, image_id=None):
        try:
            ingredient = Ingredient.objects.get(
                id=ingredient_id, is_deleted=False)
            ingredient.name = name
            ingredient.unit = unit
            ingredient.image_id = image_id
            image_service = ImageService(ingredient.created_by)
            ingredient.image_url = image_service.get_image_url(
                image_id) if image_id else None
            ingredient.save()
            return ingredient
        except Ingredient.DoesNotExist:
            raise ValueError("Ingredient not found")


class RecipeIngredientService:
    def create_recipe_ingredient(self, recipe_id, ingredient_list, created_by=None):

        if created_by is None or not isinstance(created_by, AuthUser):
            raise ValueError("A valid user must be provided")

        recipe = RecipeService().get_recipe_by_id(recipe_id)
        recipe_ingredient_list = []

        for item in ingredient_list:

            ingredient = IngredientService().get_ingredient_by_id(
                item['ingredient_id'])
            quantity = item['quantity']
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity,
                created_by=created_by)
            image_service = ImageService(created_by)
            recipe_ingredient.image_url = image_service.get_image_url(
                ingredient.image_id) if ingredient.image_id else None

            recipe_ingredient_list.append(recipe_ingredient)

        return RecipeIngredient.objects.bulk_create(recipe_ingredient_list)

    def get_recipe_ingredient_list(self, recipe_id):

        try:
            list = RecipeIngredient.objects.filter(
                recipe_id=recipe_id, is_deleted=False).order_by('-created_at')
            for recipe_ingredient in list:
                image_service = ImageService(recipe_ingredient.created_by)
                recipe_ingredient.image_url = image_service.get_image_url(
                    recipe_ingredient.ingredient.image_id) if recipe_ingredient.ingredient.image_id else None
            return list
        except RecipeIngredient.DoesNotExist:
            raise ValueError("Recipe ingredients not found")

    def delete_recipe_ingredient(self, recipe_ingredient_id):

        recipe_ingredient = RecipeIngredient.objects.filter(
            id=recipe_ingredient_id, is_deleted=False).first()
        if not recipe_ingredient:
            raise ValueError("Recipe ingredient not found")
        recipe_ingredient.is_deleted = True
        recipe_ingredient.save()
        return True

    def update_recipe_ingredient(self, recipe_ingredient_id, quantity):
        try:
            recipe_ingredient = self.get_recipe_ingredient_by_id(
                recipe_ingredient_id)
            recipe_ingredient.quantity = quantity
            recipe_ingredient.save()
            image_service = ImageService(recipe_ingredient.created_by)
            recipe_ingredient.image_url = image_service.get_image_url(
                recipe_ingredient.ingredient.image_id) if recipe_ingredient.ingredient.image_id else None

            return recipe_ingredient
        except RecipeIngredient.DoesNotExist:
            raise ValueError("Recipe ingredient not found")

    def get_recipe_ingredient_by_id(self, recipe_ingredient_id):
        try:
            recipe_ingredient = RecipeIngredient.objects.get(
                id=recipe_ingredient_id, is_deleted=False)
            image_service = ImageService(recipe_ingredient.created_by)
            recipe_ingredient.image_url = image_service.get_image_url(
                recipe_ingredient.ingredient.image_id) if recipe_ingredient.ingredient.image_id else None
            return recipe_ingredient

        except RecipeIngredient.DoesNotExist:
            raise ValueError("Recipe ingredient not found")

    def add_ingredient_to_recipe(self, recipe_id, ingredient_id, quantity, created_by=None):
        if created_by is None or not isinstance(created_by, AuthUser):
            raise ValueError("A valid user must be provided")
        recipe = RecipeService().get_recipe_by_id(recipe_id)
        ingredient = IngredientService().get_ingredient_by_id(ingredient_id)

        existing_item = RecipeIngredient.objects.filter(
            recipe=recipe, ingredient=ingredient).exists()

        if existing_item:
            existing_item.quantity = quantity
            existing_item.is_deleted = False
            existing_item.created_by = created_by
            existing_item.save()
            image_service = ImageService(created_by)
            existing_item.image_url = image_service.get_image_url(
                ingredient.image_id) if ingredient.image_id else None

            return existing_item

        else:
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity,
                created_by=created_by
            )
            recipe_ingredient.save()
            image_service = ImageService(created_by)
            recipe_ingredient.image_url = image_service.get_image_url(
                ingredient.image_id) if ingredient.image_id else None

            return recipe_ingredient
