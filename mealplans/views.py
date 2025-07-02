from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MealPlanSerializer
from .services import MealPlanService


class MealPlanView(APIView):

    def get(self, request):
        """
        Retrieves the meal plans for the authenticated user.
        """
        try:
            service = MealPlanService(user=request.user)
            meal_plans = service.get_meal_plan()
            serializer = MealPlanSerializer(meal_plans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        Creates a new meal plan for the authenticated user.
        """
        serializer = MealPlanSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = MealPlanService(user=request.user)
                meal_plan = service.create_meal_plan(
                    title=serializer.validated_data['title'],
                    start_date=serializer.validated_data['start_date'],
                    end_date=serializer.validated_data['end_date']
                )
                return Response(MealPlanSerializer(meal_plan).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealPlanDetailView(APIView):

    def put(self, request, meal_plan_id):
        """
        Updates an existing meal plan.
        """
        serializer = MealPlanSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = MealPlanService(user=request.user)
                meal_plan = service.update_meal_plan(
                    meal_plan_id=meal_plan_id,
                    title=serializer.validated_data['title'],
                    start_date=serializer.validated_data['start_date'],
                    end_date=serializer.validated_data['end_date']
                )
                return Response(MealPlanSerializer(meal_plan).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, meal_plan_id):
        """
        Deletes a meal plan by its ID.
        """
        try:
            service = MealPlanService(user=request.user)
            is_deleted = service.delete_meal_plan(meal_plan_id)
            if is_deleted is True:
                return Response({"message": "Meal plan deleted successfully"}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
