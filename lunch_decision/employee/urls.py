from .views import CreateEmployeeView
from django.urls import path

urlpatterns = [
    path(
        "create/",
        CreateEmployeeView.as_view(),
        name="create_employee",
    ),
]
