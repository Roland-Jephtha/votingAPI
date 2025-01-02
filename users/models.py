from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(default="avatar.svg", null=True)
    mobile = models.CharField(max_length=13, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender =  models.CharField(max_length=10, blank=True, null=True)
    username =  models.CharField(max_length=15, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']





class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"






# class BlacklistedToken(models.Model):
#     token = models.CharField(max_length=500)
#     blacklisted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.token









# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# from django.db import models

# class MyUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
        
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)
#     avatar = models.ImageField(default="avatar.svg", null=True)
#     mobile = models.CharField(max_length=13, blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     gender = models.CharField(max_length=10, blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
    
#     objects = MyUserManager()
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email
