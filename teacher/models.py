from django.db import models
from config.mixins import CreatedModifiedMixin
from users.models import User
# Create your models here.

class TeacherModel(CreatedModifiedMixin):
    teacher = models.ForeignKey(to=User,on_delete=models.CASCADE)
    salary = models.IntegerField(blank=True,null=True)
    subject = models.CharField(max_length=20,blank=True,null=True)


    def __str__(self):
        return str(self.teacher.first_name)