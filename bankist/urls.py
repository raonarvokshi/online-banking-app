from django.contrib import admin
from django.urls import path, include
from App.views import home, login, register, logout, profile, change_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("home/", home, name="home"),
    path("profile/", profile, name="profile"),
    path("profile/change-password/", change_password, name="change_password"),
    path("accounts/", include("allauth.urls"))
]
