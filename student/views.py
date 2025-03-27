from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view,permission_classes
from .serializers import StudentDetailsSerializer
from .models import StudentModel
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes((AllowAny,))
def StudentsListByClasswise(request):
    if request.method == 'GET':
        _std = request.query_params.get('class')
        if _std !=None:
            student_list = StudentModel.objects.filter(std=_std)
        else:
            student_list = StudentModel.objects.all()
        serializer = StudentDetailsSerializer(student_list,many=True)
        return Response(serializer.data)
