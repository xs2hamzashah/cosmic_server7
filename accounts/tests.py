from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import UserProfile

class BaseTestCase(APITestCase):
    def authenticate_user(self, email='testuser@example.com', password='password', role='seller'):
        # Create a user for authentication
        User = get_user_model()
        self.user = User.objects.create_user(
            email=email,
            full_name='Test User',
            phone_number='1234567890',
            password=password
        )

        # Create UserProfile for the user
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            role=role
        )

        # Log in the user and obtain JWT token
        response = self.client.post(reverse('login'), {
            'email': email,
            'password': password
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def setUp(self):
        # Call the helper method to authenticate a user before each test
        self.authenticate_user()
