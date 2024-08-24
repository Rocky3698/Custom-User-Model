from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from .constants import ROLE_CHOICES, GENDER_CHOICES, MEMBERSHIP_CHOICES
# Create your models here.

def is_valid_role(role)->bool:
    return role in ['admin','shelter','adopter']

class UserManager(UserManager):
    def createUser(self,email, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not is_valid_role(role):
            raise ValueError('Invalid role')
        
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def createSuperUser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('role','admin')
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email,'admin',password,**extra_fields)


class User(AbstractBaseUser):
    email                       = models.EmailField(unique=True)
    first_name                  = models.CharField(max_length=20)
    last_name                   = models.CharField(max_length=20)
    role                        = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number                = models.CharField(max_length=15, blank=True)
    date_of_birth               = models.DateField(null=True, blank=True)
    profile_picture             = models.URLField(max_length=200, blank=True, null=True)
    gender                      = models.CharField(max_length=10, choices=GENDER_CHOICES)

    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField(auto_now_add=True)
    last_modified               = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD              = 'email'
    REQUIRED_FIELDS             = []

    class Meta:
        verbose_name            = 'User'
        verbose_name_plural     = 'Users'

    def __str__(self) -> str:
        return self.email


class Address(models.Model):
    user                        = models.OneToOneField(User, on_delete=models.CASCADE)
    street                      = models.CharField(max_length=50)
    city                        = models.CharField(max_length=50)
    state                       = models.CharField(max_length=50)
    postal_code                 = models.CharField(max_length=30)
    country                     = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.user.email},{self.city},{self.country}"


class Membership(models.Model):
    user                        = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_type             = models.CharField(max_length=20,default='basic', choices=MEMBERSHIP_CHOICES)
    start_date                  = models.DateTimeField()
    end_date                    = models.DateTimeField()
