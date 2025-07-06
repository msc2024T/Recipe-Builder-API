from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient
from users.serializers import UserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    image_id = serializers.IntegerField(write_only=True, required=False)
    image_url = serializers.CharField(read_only=True, allow_null=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'created_by', 'image', 'image_url']


class IngredientSerializer(serializers.ModelSerializer):
    image_id = serializers.IntegerField(write_only=True, required=False)
    image_url = serializers.CharField(read_only=True, allow_null=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'created_by', 'image', 'image_url']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    ingredient = IngredientSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    image_url = serializers.CharField(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at',
                            'created_by', 'recipe', 'ingredient', 'image_url']


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):

    ingredient_id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient_id', 'quantity']


class RecipeIngredientUpdateSerializer(serializers.ModelSerializer):

    recipe_ingredient_id = serializers.IntegerField()
    quantity = serializers.FloatField()
