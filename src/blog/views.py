from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse

from django.views import View
from django.views.generic import ListView

from blog.models import Post
from blog.forms import PostForm

from django.utils import timezone


def home(request):
    latest_post = Post.objects.filter(published_date__date__lte=timezone.now()).order_by("-published_date")
    blogs_list = User.objects.all().order_by("-username")
    context = {'posts': latest_post, 'blogs':blogs_list}
    return render(request, "home.html", context)


def post_detail(request, username, pk):
    user = User.objects.get(username=username).pk
    possible_post = Post.objects.filter(pk=pk,user=user).select_related("category")
    if len(possible_post) == 0:
        return render(request, "404.html", status=404)
    else:
        post = possible_post[0]
        context = {'post': post}
        return render(request, "post_detail.html", context)


def blog_list(request):
    blogs_list = User.objects.all().order_by("-username")
    context = {'blogs': blogs_list}
    return render(request, "all_blogs.html", context)


class CreatePostView(LoginRequiredMixin, View):

    def get(self, request):
        form = PostForm()
        return render(request, "post_form.html", {'form': form})

    def post(self, request):
        post = Post()
        post.user = request.user
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            form = PostForm()
            url = reverse("post_detail_page", args=[post.user, post.pk])
            message = "Post created successfully! "
            message += '<a href="{0}">View</a>'.format(url)
            messages.success(request, message)
        return render(request, "post_form.html", {'form': form})


class MyPostsView(ListView):

    model = Post
    template_name = "my_posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usernam = self.kwargs.get("username")
        context['bloguser'] = usernam
        return context

    def get_queryset(self):
        usernam = self.kwargs.get("username")
        user_name = User.objects.get(username=usernam)

        user_logged = self.request.user
        if usernam != user_logged.username and not user_logged.is_superuser:
            queryset = super(MyPostsView, self).get_queryset().filter(published_date__date__lte=timezone.now()).order_by("-published_date")
        else:
            queryset = super(MyPostsView, self).get_queryset().order_by("-published_date")
        return queryset.filter(user=user_name)
