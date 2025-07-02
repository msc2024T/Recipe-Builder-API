from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient
from users.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    ingredient = IngredientSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):

    ingredient_id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient_id', 'quantity']
