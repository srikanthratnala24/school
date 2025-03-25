from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import (SignupSerializer,CustomTokenObtainPairSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import User
from .utils import send_activation_pin
import random
from student.models import StudentModel
from teacher.models import TeacherModel
# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def SignUp(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def activate_account(request):
    email = request.data.get('email')
    pin = request.data.get('pin')

    try:
        user = User.objects.get(email=email)
        if user.pin == pin:
            user.is_active = True
            if str(user.role) == "student":
                StudentModel.objects.create(student=user)
            elif str(user.role) == "teacher":
                TeacherModel.objects.create(teacher=user)
            user.pin = None  # Clear the PIN after activation
            user.save()
            return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid PIN"}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def resend_code(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
        user.pin = random.randint(100000,999999)
        user.save()
        send_activation_pin(user=user)
        return Response({"message":"Pin send successfully"})
        
    except User.DoesNotExist:
        return Response({"error":"User has not registered yet"},status=status.HTTP_400_BAD_REQUEST)

