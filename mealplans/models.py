from django.db import models
from django.contrib.auth.models import User as AuthUser


class MealPlan(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name='meal_plans'
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Meal Plan'
        verbose_name_plural = 'Meal Plans'


class MealPlanRecipe(models.Model):
    meal_plan = models.ForeignKey(
        MealPlan, on_delete=models.CASCADE, related_name='meal_plan_recipes')
    recipe = models.ForeignKey(
        'recipes.Recipe', on_delete=models.CASCADE, related_name='meal_plan_recipes')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name='meal_plan_recipe_entries'
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipe.title} on {self.date} in {self.meal_plan.title}"

    class Meta:
        verbose_name = 'Meal Plan Recipe'
        verbose_name_plural = 'Meal Plan Recipes'
