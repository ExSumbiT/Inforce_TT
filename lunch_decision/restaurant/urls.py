from .views import (
    RestaurantCreateView,
    MenuUploadView,
    CurrentDayMenuView,
    CurrentDayResultsView,
    VoteCreateView,
)
from django.urls import path

urlpatterns = [
    path(
        "create/",
        RestaurantCreateView.as_view(),
        name="create_restaurant",
    ),
    path("menu/upload/", MenuUploadView.as_view(), name="upload_menu"),
    path("menu/today/", CurrentDayMenuView.as_view(), name="current_day_menu"),
    path("vote/", VoteCreateView.as_view(), name="vote"),
    path(
        "vote/today/",
        CurrentDayResultsView.as_view(),
        name="current_day_results",
    ),
]
