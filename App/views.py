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
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "First you need to identify yourself!")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@redirect_if_not_authenticated
def home(request):
    return render(request, "index.html")


def profile(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")

        current_user = request.user
        change_data = User.objects.get(username=current_user)
        change_data.first_name = first_name
        change_data.last_name = last_name
        change_data.username = username
        change_data.email = email
        change_data.save()
        messages.success(request, "Your account was updated successfully!")
        return redirect("profile")

    return render(request, "profile.html")


def change_password(request):
    return render(request, "password.html")


@redirect_if_authenticated
def login(request):
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


@redirect_if_authenticated
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        check_duplicate_user = User.objects.filter(
            Q(username=username) | Q(email=email)
        )

        if not first_name and not last_name and not username and not email and not password:
            messages.error(request, "Please fill out all the required fields!")
            return redirect("register")

        if check_duplicate_user:
            messages.error(request, "This user already exists")
            return redirect("register")

        elif not first_name:
            messages.error(request, "Please enter your first name!")
            return redirect("register")

        elif not last_name:
            messages.error(request, "Please enter your last name!")
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

        else:
            new_user = User.objects.create_user(
                first_name=first_name, last_name=last_name,
                username=username, email=email, password=password)
            new_user.save()
            messages.success(
                request, "Your account was registered successfully! Please confirm your account by logging in!")
            return redirect("login")

    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    messages.success(request, "You logged out successfully!")
    return redirect("login")
