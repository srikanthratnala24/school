from django.urls import path
from .views import StudentsListByClasswise

urlpatterns = [
    path('students/',StudentsListByClasswise)
]
