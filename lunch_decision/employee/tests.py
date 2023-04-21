from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from employee.models import Employee
from rest_framework_simplejwt.tokens import RefreshToken


class EmployeeTests(APITestCase):
    def setUp(self):
        self.superuser = Employee.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="superpassword123",
        )
        self.user = Employee.objects.create(
            username="user",
            email="user@example.com",
            password="password123",
        )
        user_refresh = RefreshToken.for_user(self.user)
        self.user_access_token = str(user_refresh.access_token)

        refresh = RefreshToken.for_user(self.superuser)
        self.access_token = str(refresh.access_token)

    def test_user_create_employee(self):
        url = reverse("create_employee")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "first_name": "John",
            "last_name": "Doe",
            "is_restaurant": False,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}"
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_superuser_create_employee(self):
        url = reverse("create_employee")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "first_name": "John",
            "last_name": "Doe",
            "is_restaurant": False,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["username"], "testuser")
        self.assertEqual(response.json()["is_restaurant"], False)
