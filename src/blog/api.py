from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from blog.models import Post
from blog.permissions import PostsPermission
from blog.serializer import PostsListSerializer, PostSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

from django.utils import timezone


class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [PostsPermission]

    def get_queryset(self):
        user_name = self.kwargs.get('username')
        queryset = Post.objects.filter(user__username=user_name)

        user = self.request.user
        if user_name != user.username and not user.is_superuser:
            queryset = queryset.filter(published_date__date__lte=timezone.now())
        return queryset


class PostsListAPI(ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ['title', 'intro']
    ordering_fields = ['title', 'published_date']

    def get_queryset(self):
        user_name = self.kwargs.get('username')
        queryset = Post.objects.filter(user__username=user_name)

        user = self.request.user
        if user_name != user.username and not user.is_superuser:
            queryset = queryset.filter(published_date__date__lte=timezone.now()).order_by("-published_date")
        return queryset

    def get_serializer_class(self):
        return PostsListSerializer if self.request.method == "GET" else PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
