from .views import (
    CreateEmployeeView,
    RestaurantCreateView,
    MenuUploadView,
    CurrentDayMenuView,
    CurrentDayResultsView,
    VoteCreateView,
)
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
    path("upload_menu/", MenuUploadView.as_view(), name="upload_menu"),
    path("menus/today/", CurrentDayMenuView.as_view(), name="current_day_menu"),
    path("vote/", VoteCreateView.as_view(), name="create_vote"),
    path("results/today/", CurrentDayResultsView.as_view(), name="current_day_results"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
