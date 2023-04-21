from rest_framework import generics, permissions
from .models import Employee
from lunch_decision.permissions import IsSuperUser
from .serializers import EmployeeSerializer


class CreateEmployeeView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)
