from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecipeSerializer
from .services import RecipeService


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
