from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'is_datafeeder']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'email_verified', 'phone_verified']