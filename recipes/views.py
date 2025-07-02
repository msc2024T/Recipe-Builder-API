from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientService
from .services import RecipeService, IngredientService, RecipeIngredientSerializer, RecipeIngredientCreateSerializer, RecipeIngredientUpdateSerializer


class RecipeView(APIView):

    def get(self, request):
        service = RecipeService()
        recipes = service.get_recipe_list()
        serializer = RecipeSerializer(recipes, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = RecipeService()
                created_recipe = service.create_recipe(
                    title=serializer.validated_data['title'],
                    instructions=serializer.validated_data['instructions'],
                    image_path=serializer.validated_data.get('image_path'),
                    created_by=request.user
                )
                serialized_recipe = RecipeSerializer(created_recipe).data
                return Response({'data': serialized_recipe, 'message': 'Recipe created successfully'}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailView(APIView):

    def get(self, request, recipe_id):
        try:
            service = RecipeService()
            recipe = service.get_recipe_by_id(recipe_id)
            serializer = RecipeSerializer(recipe)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, recipe_id):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = RecipeService()
                updated_recipe = service.update_recipe(
                    recipe_id=recipe_id,
                    title=serializer.validated_data['title'],
                    instructions=serializer.validated_data['instructions'],
                    image_path=serializer.validated_data.get('image_path'),

                )
                serialized_recipe = RecipeSerializer(updated_recipe).data
                return Response({'data': serialized_recipe, 'message': 'Recipe updated successfully'}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        try:
            service = RecipeService()
            result = service.delete_recipe(recipe_id)
            if result is True:
                return Response({'message': 'Recipe deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to delete recipe"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class IngredientView(APIView):

    def get(self, request):

        service = IngredientService()
        ingredients = service.get_ingredient_list()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = IngredientService()
                created_ingredient = service.create_ingredient(
                    name=serializer.validated_data['name'],
                    unit=serializer.validated_data['unit'],
                    image_path=serializer.validated_data.get('image_path'),
                    created_by=request.user
                )
                serialized_ingredient = IngredientSerializer(
                    created_ingredient).data
                return Response({'data': serialized_ingredient, 'message': 'Ingredient created successfully'}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetailView(APIView):

    def get(self, request, ingredient_id):
        try:
            service = IngredientService()
            ingredient = service.get_ingredient_by_id(ingredient_id)
            serializer = IngredientSerializer(ingredient)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, ingredient_id):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = IngredientService()
                updated_ingredient = service.update_ingredient(
                    ingredient_id=ingredient_id,
                    name=serializer.validated_data['name'],
                    unit=serializer.validated_data['unit'],
                    image_path=serializer.validated_data.get('image_path'),
                )
                serialized_ingredient = IngredientSerializer(
                    updated_ingredient).data
                return Response({'data': serialized_ingredient, 'message': 'Ingredient updated successfully'}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ingredient_id):
        try:
            service = IngredientService()
            result = service.delete_ingredient(ingredient_id)
            if result is True:
                return Response({'message': 'Ingredient deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to delete ingredient"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class RecipeIngredientView(APIView):

    def post(self, request, recipe_id):
        serializer = RecipeIngredientCreateSerializer(
            data=request.data, many=True)
        if serializer.is_valid():
            try:
                service = RecipeIngredientService()
                created_recipe_ingredient = service.create_recipe_ingredient(
                    recipe_id=recipe_id,
                    ingredient_list=serializer.validated_data,
                    created_by=request.user
                )
                serialized_recipe_ingredient = RecipeIngredientSerializer(
                    created_recipe_ingredient, many=True).data
                return Response({'data': serialized_recipe_ingredient, 'message': 'Recipe ingredient created successfully'}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, recipe_id):
        try:
            service = RecipeIngredientService()
            recipe_ingredients = service.get_recipe_ingredients_by_recipe_id(
                recipe_id)
            serializer = RecipeIngredientSerializer(
                recipe_ingredients, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, recipe_id):
        try:
            recipe_ingredient_id = request.query_params.get(
                'recipe_ingredient_id')
            if not recipe_ingredient_id:
                return Response({"error": "recipe_ingredient_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            service = RecipeIngredientService()
            result = service.delete_recipe_ingredient(recipe_ingredient_id)
            if result is True:
                return Response({'message': 'Recipe ingredients deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to delete recipe ingredients"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, recipe_id):

        serializer = RecipeIngredientUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = RecipeIngredientService()
                updated_recipe_ingredient = service.update_recipe_ingredient(
                    recipe_ingredient_id=serializer.validated_data['recipe_ingredient_id'],
                    quantity=serializer.validated_data['quantity']
                )
                serialized_recipe_ingredient = RecipeIngredientSerializer(
                    updated_recipe_ingredient).data
                return Response({'data': serialized_recipe_ingredient, 'message': 'Recipe ingredient updated successfully'}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddSingleRecipeIngredientView(APIView):

    def post(self, request, recipe_id):
        serializer = RecipeIngredientCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = RecipeIngredientService()
                created_recipe_ingredient = service.add_ingredient_to_recipe(
                    recipe_id=recipe_id,
                    ingredient_id=serializer.validated_data['ingredient_id'],
                    quantity=serializer.validated_data['quantity'],
                    created_by=request.user
                )
                serialized_recipe_ingredient = RecipeIngredientSerializer(
                    created_recipe_ingredient).data
                return Response({'data': serialized_recipe_ingredient, 'message': 'Recipe ingredient created successfully'}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
