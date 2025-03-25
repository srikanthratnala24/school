from django.db import models
from config.mixins import CreatedModifiedMixin
from users.models import User
from teacher.models import TeacherModel
# Create your models here.
CLASS_CHOICES = (
    ('Nursery','Nursery'),
    ('LKG','LKG'),
    ('UKG','UKG'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
)
class StudentModel(CreatedModifiedMixin):
    student = models.ForeignKey(to=User,on_delete=models.CASCADE)
    std = models.CharField(choices=CLASS_CHOICES, max_length=50,blank=True)
    class_teacher = models.ForeignKey(to=TeacherModel,on_delete=models.CASCADE,blank=True,null=True)
    fee = models.DecimalField(decimal_places=2,max_digits=9,blank=True,null=True)
    discount = models.IntegerField(blank=True,null=True)
    rank = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.student.first_name)
