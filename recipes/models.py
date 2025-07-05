from django.db import models
from django.contrib.auth.models import User as AuthUser
from images.models import Image


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='recipes', blank=True, null=True)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name='recipes'
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    image_path = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name='ingredients'
    )

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')
    quantity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name} in {self.recipe.title}"

    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'
