"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog.api import PostDetailAPI, PostsListAPI
from blog.views import post_detail, MyPostsView, home, CreatePostView, blog_list
from users.api import UsersListAPI, UsersDetailAPI, UsersBlogsAPI
from users.views import LoginView, logout, SignupView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login', LoginView.as_view(), name="login_page"),
    path('logout', logout, name="logout_page"),
    path('signup', SignupView.as_view(), name="signup_page"),

    path('new-post', CreatePostView.as_view(), name="create_post_page"),
    path('blogs/', blog_list, name="blogs_list_page"),
    path('blogs/<username>/<int:pk>', post_detail, name="post_detail_page"),
    path('blogs/<username>', MyPostsView.as_view(), name="post_by_blog_page"),

    path('', home, name="home_page"),

    # API REST
    path('api/1.0/users/<int:pk>', UsersDetailAPI.as_view(), name="api_users_detail"),
    path('api/1.0/users/', UsersListAPI.as_view(), name="api_users_list"),
    path('api/1.0/blogs/', UsersBlogsAPI.as_view(), name="api_users_blogs"),

    path('api/1.0/blog/<str:username>/<int:pk>', PostDetailAPI.as_view(), name="api_blog_post_detail"),
    path('api/1.0/blog/<str:username>/', PostsListAPI.as_view(), name="api_blog_post_list")
]
