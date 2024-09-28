from django.db import models

# Create your models here.a
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # business_name = models.CharField(max_length=255, blank=True, null=True)  # For sellers
    # city = models.CharField(max_length=100, blank=True, null=True)  # For buyers

    def __str__(self):
        return f'{self.user.username} - {self.role}'
