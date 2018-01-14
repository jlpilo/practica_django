from rest_framework.permissions import BasePermission


class PostsPermission(BasePermission):

    def has_permission(self, request, view):
        return request.method == "GET" or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method == "GET" or obj.user == request.user or request.user.is_superuser
