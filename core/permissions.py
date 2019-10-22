from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser or request.method == 'GET':
            return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser or request.method == 'GET':
            return True


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True
