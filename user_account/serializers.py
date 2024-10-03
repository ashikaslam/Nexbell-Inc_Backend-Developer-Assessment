#from user_profile.models import UserProfile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError  # Correct import


User = get_user_model()

class UserSerializer(serializers.ModelSerializer): 
   
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# login............................
class LoginSerializer(serializers.Serializer):  # 4
   
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, style={'input_type': 'password'})


class logoutSerializer(serializers.Serializer):  # 8
    refresh_token = serializers.CharField(write_only=True, required=True)


# to varify otp
class otp_taker(serializers.Serializer):  # 2
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    token1 =serializers.CharField()
    token2 =serializers.CharField()
    
    

# passwrod change with current password

class PasswordChangeSerializer(serializers.Serializer):  # 5
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)