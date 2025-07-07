from .models import MealPlan, MealPlanRecipe
from recipes.services import RecipeService
from images.services import ImageService


class MealPlanService:
    def __init__(self, user=None):
        if user is None:
            raise ValueError("User must be provided")
        self.user = user

    def get_meal_plan(self):
        """
        Retrieves the meal plans for the user.
        """
        meal_plans = MealPlan.objects.filter(
            created_by=self.user, is_deleted=False).order_by('-created_at')

        if not meal_plans:
            raise ValueError("No meal plans found for the user.")

        return meal_plans

    def create_meal_plan(self, title, start_date, end_date):
        """
        Creates a new meal plan for the user.
        """
        if not title or not start_date or not end_date:
            raise ValueError("Title, start date, and end date are required.")

        meal_plan = MealPlan.objects.create(
            title=title,
            start_date=start_date,
            end_date=end_date,
            created_by=self.user
        )

        return meal_plan

    def delete_meal_plan(self, meal_plan_id):
        """
        Deletes a meal plan by its ID.
        """
        try:
            meal_plan = self.get_meal_plan_by_id(meal_plan_id)
            meal_plan.is_deleted = True
            meal_plan.save()
            return True
        except MealPlan.DoesNotExist:
            raise ValueError(
                "Meal plan not found or does not belong to the user.")

    def get_meal_plan_by_id(self, meal_plan_id):
        """
        Retrieves a meal plan by its ID.
        """
        try:
            meal_plan = MealPlan.objects.get(
                id=meal_plan_id, is_deleted=False, created_by=self.user)
            return meal_plan
        except MealPlan.DoesNotExist:
            raise ValueError(
                "Meal plan not found or does not belong to the user.")

    def update_meal_plan(self, meal_plan_id, title, start_date, end_date):
        """
        Updates an existing meal plan.
        """
        try:
            meal_plan = self.get_meal_plan_by_id(meal_plan_id)

            if not title or not start_date or not end_date:
                raise ValueError(
                    "Title, start date, and end date are required.")

            meal_plan.title = title
            meal_plan.start_date = start_date
            meal_plan.end_date = end_date
            meal_plan.save()
            return meal_plan
        except ValueError as e:
            raise ValueError(f"Failed to update meal plan: {str(e)}")


class MealPlanRecipeService:
    def __init__(self, user=None):
        if user is None:
            raise ValueError("User must be provided")
        self.user = user

    def add_recipe_to_meal_plan(self, meal_plan_id, list):
        """
        Adds a recipe to a meal plan.
        """
        if not meal_plan_id or not list:
            raise ValueError("Meal plan ID and recipe list are required.")

        result = []
        meal_plan = MealPlanService(
            self.user).get_meal_plan_by_id(meal_plan_id)

        for item in list:
            recipe_id = item.get('recipe_id')

            if not recipe_id:
                raise ValueError(
                    "Recipe ID and meal type are required for each item.")

            recipe = RecipeService().get_recipe_by_id(recipe_id)

            # Check if the recipe already exists in the meal plan
            existing_item = MealPlanRecipe.objects.filter(
                meal_plan=meal_plan,
                recipe=recipe,

                is_deleted=False
            ).first()

            if existing_item:
                existing_item.is_deleted = False
                existing_item.save()
                result.append(existing_item)
            else:
                # Create a new MealPlanRecipe entry if it doesn't exist
                meal_plan_recipe = MealPlanRecipe.objects.create(
                    meal_plan=meal_plan,
                    recipe=recipe,

                    created_by=self.user
                )
                result.append(meal_plan_recipe)

        return result

    def get_meal_plan_recipes(self, meal_plan_id):
        """
        Retrieves the recipes for a specific meal plan.
        """
        meal_plan = MealPlanService(
            self.user).get_meal_plan_by_id(meal_plan_id)

        meal_plan_recipes = MealPlanRecipe.objects.filter(
            meal_plan=meal_plan, is_deleted=False
        ).select_related('recipe')

        for recipe in meal_plan_recipes:
            image_id = recipe.recipe.image_id if recipe.recipe else None
            image_service = ImageService(recipe.created_by)
            image_url = image_service.get_image_url(
                image_id) if image_id else None

            recipe.image_url = image_url

        if not meal_plan_recipes:
            raise ValueError("No recipes found for the specified meal plan.")

        return meal_plan_recipes

    def delete_meal_plan_recipe(self, meal_plan_recipe_id):
        """
        Deletes a meal plan recipe by its ID.
        """
        try:
            meal_plan_recipe = MealPlanRecipe.objects.get(
                id=meal_plan_recipe_id, created_by=self.user, is_deleted=False)
            meal_plan_recipe.is_deleted = True
            meal_plan_recipe.save()
            return True
        except MealPlanRecipe.DoesNotExist:
            raise ValueError(
                "Meal plan recipe not found or does not belong to the user.")
