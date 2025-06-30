from .dtos import UserDTO
from django.contrib.auth.models import User as AuthUser


class UserService:

    def signup(self, email, password, first_name, last_name):

        if not email or not password or not first_name or not last_name:
            raise ValueError("All fields are required")

        # check if email already exists
        if AuthUser.objects.filter(email=email).exists():
            raise ValueError("Email already exists")

        # save user to database
        user = AuthUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.save()

        # return user dto
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
