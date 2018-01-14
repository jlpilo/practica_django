from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from users.permissions import UsersPermission
from users.serializers import UserSerializer, UsersListSerializer, BlogsListSerializer


class UsersListAPI(ListCreateAPIView):

    queryset = User.objects.all()
    permission_classes = [UsersPermission]

    def get_serializer_class(self):
        return UsersListSerializer if self.request.method == "GET" else UserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UsersDetailAPI(RetrieveUpdateDestroyAPIView):

    permission_classes = [UsersPermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UsersPermission]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UsersBlogsAPI(APIView):

    def get(self, request):
        users = User.objects.all()
        paginator = PageNumberPagination()
        # paginamos el queryset
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = BlogsListSerializer(paginated_users, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
