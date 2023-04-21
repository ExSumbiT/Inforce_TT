from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers
    to create an employee and restaurant
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsRestaurant(permissions.BasePermission):
    """
    Custom permission to only allow restaurant users to access certain views
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_restaurant
        )


class IsNotRestaurant(permissions.BasePermission):
    """
    Custom permission to only allow staff users to access certain views
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and not request.user.is_restaurant
        )
