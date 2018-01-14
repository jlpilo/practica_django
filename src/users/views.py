from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm

from users.forms import LoginForm, SignUpForm


class LoginView(View):

    def get(self, request):
        context = {'form': LoginForm()}
        return render(request, "login_form.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("login_username")
            password = form.cleaned_data.get("login_password")
            #form.save()
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user and authenticated_user.is_active:
                django_login(request, authenticated_user)
                redirect_to = request.GET.get("next", "home_page")
                return redirect(redirect_to)
            else:
                form.add_error(None, "Usuario incorrecto o inactivo")
        context = {'form': form}
        return render(request, "login_form.html", context)


class SignupView(View):
    def get(self, request):
        context = {'form': SignUpForm()}
        return render(request, "signup_form.html", context)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            django_login(request, user)
            return redirect('home_page')
        else:
            form.add_error(None, "Datos no válidos")
        return render(request, 'signup_form.html', {'form': form})


def logout(request):
    django_logout(request)
    return redirect("login_page")
