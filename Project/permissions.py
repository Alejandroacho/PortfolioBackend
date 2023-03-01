from django.http import HttpRequest
from rest_framework.permissions import BasePermission


class IsGetPetition(BasePermission):
    message: str = "You don't have permission"

    def has_permission(self, request: HttpRequest, _) -> bool:
        return request.method == "GET"
