import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from restaurant.models import Restaurant, Menu, Vote
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def employee_user():
    user = get_user_model().objects.create_user(
        username="employeeuser",
        password="testpassword123",
        is_restaurant=False,
    )
    return user


@pytest.fixture
def restaurant_user():
    user = get_user_model().objects.create_user(
        username="restaurantuser",
        password="testpassword123",
        is_restaurant=True,
    )
    return user


@pytest.fixture
def restaurant(restaurant_user):
    restaurant = Restaurant.objects.create(
        employee=restaurant_user,
        name="Test Restaurant",
        address="123 Test St",
        description="A test restaurant",
    )
    return restaurant


@pytest.fixture
def menu(restaurant):
    menu = Menu.objects.create(
        restaurant=restaurant,
        date="2022-10-01",
        items="Menu items for test",
    )
    return menu


@pytest.fixture
def vote(employee_user, menu):
    vote = Vote.objects.create(
        employee=employee_user,
        menu=menu,
        date="2022-10-01",
    )
    return vote


# Test Employee creation
def test_create_employee(api_client):
    url = reverse("employee-create")
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "first_name": "John",
        "last_name": "Doe",
        "is_restaurant": False,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "testuser"
