from rest_framework import permissions
from rest_framework.authtoken.models import Token


class OwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        token_user = Token.objects.get(key=token).user
        return user == token_user

