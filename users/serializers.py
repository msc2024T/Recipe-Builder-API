from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser

# Serializer for user signup


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, min_length=8, max_length=30)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
