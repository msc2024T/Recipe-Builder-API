from rest_framework import serializers
from .models import MealPlan, MealPlanRecipe
from users.serializers import UserSerializer
from recipes.serializers import RecipeSerializer


class MealPlanSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = MealPlan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
