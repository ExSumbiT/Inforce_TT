from django.urls import path, include


urlpatterns = [
    path("api/v1/auth/", include("token_auth.urls")),
    path("api/v1/employee/", include("employee.urls")),
    path("api/v1/restaurant/", include("restaurant.urls")),
    # ...
]
