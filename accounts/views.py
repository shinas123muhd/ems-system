from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ProfileUpdateForm


def login_view(request):
    return render(request, "accounts/login.html")

def register_view(request):
    return render(request, "accounts/register.html")
    



def logout_view(request):
    logout(request)
    return redirect('login')



def profile_view(request):
    return render(request, 'accounts/profile.html')



def change_password_view(request):
    return render(request, 'accounts/change_password.html')
