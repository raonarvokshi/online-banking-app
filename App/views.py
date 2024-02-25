from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q


def redirect_if_authenticated(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def redirect_if_not_authenticated(view_func):
    def _wraped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to identify yourself first!")
            return redirect("home")

        return view_func(request, *args, **kwargs)
    return _wraped_view


def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to identify yourself first!")
        return redirect("login")
    return render(request, "index.html")


def login(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already loged in")
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)

        if not username and not password:
            messages.error(request, "Please fill out all the required fields!")
            return redirect("login")

        elif not username:
            messages.error(request, "Please enter your username!")
            return redirect("login")

        elif not password:
            messages.error(request, "Please enter your password!")

        else:
            if user is not None:
                auth.login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Incorrect Credentials")
                return redirect("login")

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        check_duplicate_user = User.objects.filter(
            Q(username=username) | Q(email=email)
        )

        if check_duplicate_user:
            messages.error(request, "This user already exists")
            return redirect("register")

        if not username and not email and not password and not confirm_password:
            messages.error(request, "Please fill out all the required fields!")
            return redirect("register")

        elif not username:
            messages.error(request, "Please enter your username!")
            return redirect("register")

        elif not email:
            messages.error(request, "Please enter your email!")
            return redirect("register")

        elif not password:
            messages.error(request, "Please enter your password!")
            return redirect("register")

        elif not confirm_password:
            messages.error(request, "Please confirm your password!")
            return redirect("register")

        elif password != confirm_password:
            messages.error(request, "Please enter the same password!")
            return redirect("register")

        else:
            new_user = User.objects.create_user(
                username=username, email=email, password=password)
            new_user.save()
            messages.success(
                request, "Your account was registered successfully! Please confirm your account by logging in!")
            return redirect("login")

    return render(request, "register.html")
