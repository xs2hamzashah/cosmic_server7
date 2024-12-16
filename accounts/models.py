from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, AbstractUser
from django.db import models

from core.models import TimeStampedModel
from cosmic_server7 import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, TimeStampedModel):
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    _user_profile_id_cache = None  # Initialize a private cache variable

    @property
    def userprofile_id(self):
        # Check if the UserProfile is already cached
        if self._user_profile_id_cache is None:
            try:
                self._user_profile_id_cache = self.userprofile.id  # Lazy load and cache the UserProfile
            except UserProfile.DoesNotExist:
                self._user_profile_id_cache = None  # Handle the case where the UserProfile does not exist
        return self._user_profile_id_cache

    def __str__(self):
        return self.email


class UserProfile(TimeStampedModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        SELLER = 'seller', 'Seller'
        BUYER = 'buyer', 'Buyer'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices)

    _user_id_cache = None  # Initialize a private cache variable

    @property
    def user_id(self):
        # Check if user_id is already cached
        if self._user_id_cache is None:
            self._user_id_cache = self.user.id  # Lazy load and cache the user_id
        return self._user_id_cache

    def __str__(self):
        return f'{self.user.username} - {self.role}'


class Company(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='company')
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name