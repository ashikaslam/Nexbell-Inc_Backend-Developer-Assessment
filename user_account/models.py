from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
import datetime




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    # user will submit
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
   
    
    # others
    date_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
#................. X ....................................
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    
    
    
    
# security >>>>>>>>code





class Email_varification(models.Model):
    email = models.EmailField()
    otp =models.IntegerField()
    token1=models.CharField( max_length=30)
    token2=models.CharField( max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_otp_valid(self):
        now = timezone.now()
        return (now - self.created_at) < datetime.timedelta(minutes=10)
    
    
