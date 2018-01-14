from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class LoginForm(forms.Form):

    login_username = forms.CharField(label="Username")
    login_password = forms.CharField(widget=forms.PasswordInput(), label="Password")


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label="Blog Name")
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(max_length=254, help_text=mark_safe('<ul><li>Your password can&#39;t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can&#39;t be a commonly used password.</li><li>Your password can&#39;t be entirely numeric.</li></ul>'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )