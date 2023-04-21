from rest_framework import generics, permissions
from django.db.models import Count
from .models import Restaurant, Menu, Vote
from lunch_decision.permissions import (
    IsSuperUser,
    IsRestaurant,
    IsNotRestaurant,
)
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    VoteSerializer,
)
from datetime import date


class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)


class MenuUploadView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAuthenticated, IsRestaurant)

    def perform_create(self, serializer):
        # Retrieve the authenticated user's restaurant
        restaurant = Restaurant.objects.get(employee=self.request.user)
        today = date.today()
        serializer.save(restaurant=restaurant, date=today)


class CurrentDayMenuView(generics.ListAPIView):
    queryset = Menu.objects.filter(date=date.today())
    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAuthenticated, IsNotRestaurant)


class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticated, IsNotRestaurant)

    def perform_create(self, serializer):
        employee = self.request.user
        today = date.today()
        serializer.save(employee=employee, date=today)


class CurrentDayResultsView(generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        today = date.today()
        # Get the menus for the current day
        queryset = Menu.objects.filter(date=today)

        # Annotate the queryset with the count of votes for each menu
        queryset = queryset.annotate(vote_count=Count("vote"))

        return queryset
