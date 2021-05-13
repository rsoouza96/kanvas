from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        
        if (request.user and request.user.is_authenticated):
            return bool(request.user.is_superuser)


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        elif request.method == 'POST':
            if request.user and request.user.is_authenticated:
                if not request.user.is_superuser and not request.user.is_staff:
                    return True
                else:
                    raise NotAuthenticated()

        elif request.user and request.user.is_authenticated:
            if request.user.is_staff:
                return True
            else:
                raise NotAuthenticated()