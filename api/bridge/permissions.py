from rest_framework import permissions
from django.contrib.auth.models import User, Group, AnonymousUser


class IsOwnerNotPatchOrPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_superuser:
            return True
        if request.method == 'POST' and type(request.user) != AnonymousUser:
            return True
        # Instance must have an attribute named `owner`.
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if (request.method in permissions.SAFE_METHODS) or request.user.is_superuser:
        if request.user.is_superuser:
            return True
        # Instance must have an attribute named `owner`.
        if obj.username == request.user.username:
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.method == 'DELETE' and type(request.user) != AnonymousUser:
                return True
        return False


class ForChatSend(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_superuser:
            return True
        if request.method == 'POST' and type(request.user) != AnonymousUser and request.data['send'] == request.user.username:
            return True
        if request.method in permissions.SAFE_METHODS and type(request.user) != AnonymousUser and request.data['send'] == request.user.username:
            return True
        # Instance must have an attribute named `owner`.
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if (request.method in permissions.SAFE_METHODS) or request.user.is_superuser:
        if request.user.is_superuser:
            return True
        # Instance must have an attribute named `owner`.

        if obj.send == request.user.username:
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.method == 'DELETE':
                return True
        return False


class ForChatReceive(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_superuser:
            return True
        # if request.method == 'POST' and type(request.user) != AnonymousUser and request.data['send'] == request.user.username:
        #     return True
        # Instance must have an attribute named `owner`.
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if (request.method in permissions.SAFE_METHODS) or request.user.is_superuser:
        if request.user.is_superuser:
            return True
        # Instance must have an attribute named `owner`.
        if obj.receive == request.user.username:
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.method == 'DELETE':
                return True
        return False


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if (request.method in permissions.SAFE_METHODS) or request.user.is_superuser:
        if request.user.is_superuser:
            return True
        # Instance must have an attribute named `owner`.
        return obj.username == request.user.username


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if (request.method in permissions.SAFE_METHODS) or request.user.is_superuser:
        if request.user.is_superuser:
            return True
        # Instance must have an attribute named `owner`.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.username == request.user.username


class AnonymousUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_superuser:
            return True
        if request.method == 'POST' and type(request.user) != AnonymousUser:
            return False
        # Instance must have an attribute named `owner`.
        return True
