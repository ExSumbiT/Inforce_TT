from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Employee


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
