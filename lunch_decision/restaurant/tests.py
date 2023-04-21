from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from employee.models import Employee
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Menu, Restaurant, Vote
from datetime import date


def create_user():
    user = Employee.objects.get_or_create(
        username="user",
        email="user@example.com",
        password="password123",
    )[0]
    user_refresh = RefreshToken.for_user(user)
    user_access_token = str(user_refresh.access_token)
    return user, user_access_token


def create_superuser():
    if Employee.objects.filter(username="superuser").exists():
        superuser = Employee.objects.filter(username="superuser").first()
    else:
        superuser = Employee.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="superpassword123",
        )
    superuser_refresh = RefreshToken.for_user(superuser)
    superuser_access_token = str(superuser_refresh.access_token)
    return superuser, superuser_access_token


def create_restaurant_user():
    restaurant_user = Employee.objects.get_or_create(
        username="restaurant_user",
        email="restaurant_user@example.com",
        password="restaurantpassword123",
        is_restaurant=True,
    )[0]
    restaurant_user_refresh = RefreshToken.for_user(restaurant_user)
    restaurant_user_access_token = str(restaurant_user_refresh.access_token)
    return restaurant_user, restaurant_user_access_token


class RestaurantTests(APITestCase):
    def setUp(self):
        self.superuser, self.superuser_access_token = create_superuser()
        self.user, self.user_access_token = create_user()

    # Test Restaurant creation
    def test_user_create_restaurant(self):
        url = reverse("create_restaurant")
        data = {
            "name": "Test Restaurant",
            "address": "123 Test St",
            "description": "A test restaurant",
            "employee_username": "testrestaurant",
            "employee_password": "testpassword123",
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}"
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_superuser_create_restaurant(self):
        url = reverse("create_restaurant")
        data = {
            "name": "Test Restaurant",
            "address": "123 Test St",
            "description": "A test restaurant",
            "employee_username": "testrestaurant",
            "employee_password": "testpassword123",
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.superuser_access_token}"
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "Test Restaurant"
        assert response.json()["address"] == "123 Test St"


class MenuTests(APITestCase):
    def setUp(self):
        self.user, self.user_access_token = create_user()
        (
            self.restaurant_user,
            self.restaurant_user_access_token,
        ) = create_restaurant_user()
        self.restaurant = Restaurant.objects.create(
            employee=self.restaurant_user,
            name="Test Restaurant",
            address="123 Test St",
        )

    # Test Menu uploading
    def test_user_upload_menu(self):
        url = reverse("upload_menu")
        data = {
            "restaurant": self.restaurant.id,
            "items": "Test menu items",
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}"
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_restaurant_user_upload_menu(self):
        url = reverse("upload_menu")
        data = {
            "restaurant": self.restaurant.id,
            "items": "Test menu items",
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.restaurant_user_access_token}"
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["items"] == "Test menu items"

    def test_double_restaurant_user_upload_menu(self):
        Menu.objects.create(
            restaurant=self.restaurant,
            date=date.today(),
            items="Menu items for test",
        )
        url = reverse("upload_menu")
        data = {
            "restaurant": self.restaurant.id,
            "items": "Test menu items",
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.restaurant_user_access_token}"
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        url = reverse("current_day_menu")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}"
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # Test getting current day menu
    def test_user_get_current_day_menu(self):
        Menu.objects.create(
            restaurant=self.restaurant,
            date=date.today(),
            items="Menu items for test",
        )
        url = reverse("current_day_menu")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}"
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["items"] == "Menu items for test"

    def test_restaurant_user_get_current_day_menu(self):
        url = reverse("current_day_menu")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.restaurant_user_access_token}"
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class VoteTests(APITestCase):
    def setUp(self):
        self.superuser, self.superuser_access_token = create_superuser()
        self.user, self.user_access_token = create_user()
        (
            self.restaurant_user,
            self.restaurant_user_access_token,
        ) = create_restaurant_user()
        self.restaurant = Restaurant.objects.create(
            employee=self.restaurant_user,
            name="Test Restaurant",
            address="123 Test St",
        )
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            date=date.today(),
            items="Menu items for test",
        )

    # Test voting
    def test_user_vote(self):
        url = reverse("vote")
        data = {
            "employee": self.user.id,
            "menu": self.menu.id,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}"
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["employee"] == self.user.id

    def test_double_user_vote(self):
        Vote.objects.create(
            employee=self.user, menu=self.menu, date=date.today()
        )
        url = reverse("vote")
        data = {
            "employee": self.user.id,
            "menu": self.menu.id,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}"
        )
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test getting current day results
    def test_get_current_day_results(self):
        Vote.objects.create(
            employee=self.user, menu=self.menu, date=date.today()
        )
        url = reverse("current_day_results")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}"
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["vote_count"] == 1
