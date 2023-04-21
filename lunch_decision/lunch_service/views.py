from rest_framework import generics, permissions
from .models import Employee, Restaurant, Menu, Vote
from .permissions import IsSuperUser, IsRestaurant
from .serializers import (
    EmployeeSerializer,
    RestaurantSerializer,
    MenuSerializer,
    VoteSerializer,
)
from datetime import date


class CreateEmployeeView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)


class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)


class MenuUploadView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAuthenticated, IsRestaurant)


class CurrentDayMenuView(generics.ListAPIView):
    queryset = Menu.objects.filter(date=date.today())
    serializer_class = MenuSerializer


class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CurrentDayResultsView(generics.ListAPIView):
    queryset = Vote.objects.filter(date=date.today())
    serializer_class = VoteSerializer
