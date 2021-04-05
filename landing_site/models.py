from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class SupportModel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=64)
    message = models.TextField()
    date_received = models.DateField(auto_now_add=True)

    def full_name(self):
        return f'{first_name} {last_name}'

class AccountManagerModel(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('User must have an email address!')
        if not username:
            raise ValueError('User must have an username!')
        
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError('User must have an email address!')
        if not username:
            raise ValueError('User must have an username!')
        
        user = self.create_user(email=self.normalize_email(email), username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class AccountModel(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=254, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=254)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Active', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = AccountManagerModel()

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

