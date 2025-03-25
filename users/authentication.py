from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user = get_user_model().objects.get(email=validated_token["email"])
            return user
        except get_user_model().DoesNotExist:
            return None
