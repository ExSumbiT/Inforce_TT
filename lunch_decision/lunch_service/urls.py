from .views import CreateEmployeeView, RestaurantCreateView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ... other urlpatterns
    path("create_employee/", CreateEmployeeView.as_view(), name="create_employee"),
    path(
        "create_restaurant/", RestaurantCreateView.as_view(), name="create_restaurant"
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
