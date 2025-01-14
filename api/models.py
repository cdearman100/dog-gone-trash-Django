from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group, Permission,  BaseUserManager

class TrashLocation(models.Model):
    name = models.CharField(max_length=100)
    date_of_event = models.DateField()
    description = models.TextField(blank=True, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    users_joined = models.ManyToManyField('User', related_name='joined_locations', blank=True)

    def __str__(self):
        return self.name
    
    
class Reward(models.Model):
    name = models.CharField(max_length=255)  # Name of the reward
    description = models.TextField(blank=True, null=True)  # Description of the reward
    points = models.PositiveIntegerField()  # Points required to redeem the reward
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-filled when created
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updated on save


class UserManager(BaseUserManager):
    """
    Custom manager for the User model that uses email as the unique identifier.
    """
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        if password:
            user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model that replaces the username field with email.
    """
    username = None  # Remove the default username field
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    reward_points = models.PositiveIntegerField(default=0)  # Add reward points field

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['full_name']  # Required fields besides email

    objects = UserManager()  # Link the custom manager to the User model

    def __str__(self):
        return self.email