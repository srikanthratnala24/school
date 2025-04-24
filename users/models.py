from django.db import models
from config.mixins import CreatedModifiedMixin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
import random


# Create your models here.
ROLE_CHOICES =(
    ('admin',"admin"),
    ('student',"student"),
    ('teacher',"teacher"),
    ('staff',"staff"),
    ('adminstrator',"adminstrator"),
)

class Roles(models.Model):
    role = models.CharField(max_length=13,choices=ROLE_CHOICES)

    def __str__(self):
        return self.role
    

class User(CreatedModifiedMixin, AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("email_address"),unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    first_name = models.CharField(max_length=25,blank=False)
    last_name = models.CharField(max_length=25,blank=False)
    # role = models.ForeignKey(Roles,on_delete=models.CASCADE,blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    pin = models.CharField(max_length=6,blank=True,null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def generate_pin(self):
        self.pin = str(random.randint(100000,999999))
        self.save()