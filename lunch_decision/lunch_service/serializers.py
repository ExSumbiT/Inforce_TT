from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Employee, Restaurant, Menu, Vote
from datetime import date


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_restaurant",
        )
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "username": {
                "validators": [
                    UniqueValidator(queryset=Employee.objects.all())
                ]
            },
        }

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)


class RestaurantSerializer(serializers.ModelSerializer):
    employee_username = serializers.CharField(
        max_length=150,
        write_only=True,
    )
    employee_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "address",
            "description",
            "employee_username",
            "employee_password",
        )
        extra_kwargs = {
            "description": {"required": False},
        }

    def validate_employee_username(self, value):
        if Employee.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user for this restaurant already exists."
            )
        return value

    def create(self, validated_data):
        # Extract the username and password fields from validated_data
        employee_username = validated_data.pop("employee_username")
        employee_password = validated_data.pop("employee_password")

        # Create a new Employee object for the restaurant
        employee = Employee.objects.create_user(
            username=employee_username,
            password=employee_password,
            is_restaurant=True,
        )

        # Set the newly created employee as the employee for the restaurant
        validated_data["employee"] = employee

        # Create the new Restaurant object
        return super().create(validated_data)


class RestaurantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "address", "description")


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantDetailSerializer(read_only=True)
    vote_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Menu
        fields = (
            "id",
            "restaurant",
            "date",
            "items",
            "vote_count",
        )
        extra_kwargs = {
            "date": {"required": False},
        }

    def validate_unique_restaurant_and_date(self, attrs):
        restaurant = Restaurant.objects.get(
            employee=self.context["request"].user
        )
        menu_date = attrs.get("date", date.today())

        if Menu.objects.filter(restaurant=restaurant, date=menu_date).exists():
            raise serializers.ValidationError(
                "A menu from this restaurant already exists for this date."
            )
        return attrs

    def validate(self, attrs):
        attrs = self.validate_unique_restaurant_and_date(attrs)
        return attrs


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = (
            "id",
            "employee",
            "menu",
            "date",
        )
        extra_kwargs = {
            "employee": {"required": False},
            "date": {"required": False},
        }

    def validate_unique_employee_and_date(self, attrs):
        employee = self.context["request"].user
        menu = attrs["menu"]
        vote_date = attrs.get("date", date.today())

        if Vote.objects.filter(
            employee=employee, menu=menu, date=vote_date
        ).exists():
            raise serializers.ValidationError(
                "You have already voted for this menu today."
            )
        return attrs

    def validate(self, attrs):
        attrs = self.validate_unique_employee_and_date(attrs)
        return attrs
