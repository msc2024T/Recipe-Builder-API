from .models import MealPlan


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
            created_by=self.user).order_by('-created_at')

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
