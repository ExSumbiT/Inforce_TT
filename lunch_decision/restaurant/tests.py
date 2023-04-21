from django.urls import reverse
from rest_framework import status


# Test Restaurant creation
def test_create_restaurant(api_client, employee_user):
    api_client.force_authenticate(user=employee_user)
    url = reverse("restaurant-create")
    data = {
        "name": "Test Restaurant",
        "address": "123 Test St",
        "description": "A test restaurant",
        "employee_username": "testrestaurant",
        "employee_password": "testpassword123",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Test Restaurant"


# Test Menu uploading
def test_upload_menu(api_client, restaurant_user):
    api_client.force_authenticate(user=restaurant_user)
    url = reverse("menu-upload")
    data = {
        "restaurant": restaurant_user.restaurant.id,
        "items": "Test menu items",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["items"] == "Test menu items"


# Test getting current day menu
def test_get_current_day_menu(api_client, menu):
    url = reverse("current-day-menu")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["items"] == "Menu items for test"


# Test voting
def test_create_vote(api_client, employee_user, menu):
    api_client.force_authenticate(user=employee_user)
    url = reverse("vote-create")
    data = {
        "employee": employee_user.id,
        "menu": menu.id,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["employee"] == employee_user.id


# Test getting current day results
def test_get_current_day_results(api_client, menu, vote):
    url = reverse("current-day-results")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["vote_count"] == 1
