from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, UserSerializer
from .services import UserService


class UserSignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():

            try:
                service = UserService()

                created_user = service.signup(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name']
                )

                if created_user:
                    serialized_user = UserSerializer(created_user).data

                    return Response({'data': serialized_user, 'message': 'user created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "User creation failed"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
