from rest_framework import serializers
from .models import User,Roles
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .utils import send_activation_pin


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=24)
    last_name = serializers.CharField(max_length=24)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all())
    email = serializers.EmailField()

    def create(self, validated_data):
        validated_data.pop('confirm_password','None')
        password = validated_data.pop('password','None')
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.generate_pin()
        user.save()
        send_activation_pin(user)
        return user
        
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password and confirm password should match")
        return attrs




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise AuthenticationFailed("Incorrect password")
            if not user.is_active:
                raise AuthenticationFailed("User is not active")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return super().validate(attrs)
