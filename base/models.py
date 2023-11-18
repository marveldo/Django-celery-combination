

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault('is_admin',True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
    
class Myuser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, blank = True, null = True, unique = True)
    email = models.EmailField( unique=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Product(models.Model):
    name = models.CharField( blank=False, null = False ,max_length=200, default='default+product')
    product_price = models.DecimalField(decimal_places=7, max_digits=30 ,default = 0.00, blank=False, null=False)
    product_about = models.TextField(default = 'blank', blank=False, null = False)
    is_featured = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, blank =True, null= True, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=220, blank =True, null=True)
    customer_address = models.CharField(max_length=400, blank=True,null=True)
    customer_number = PhoneNumberField(null = True,blank=True)
    is_complete = models.BooleanField(default=False,blank=True,null = True)

    def __str__(self):
        return f'{self.customer_name} ordered {self.product}'
        