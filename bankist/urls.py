from django.contrib import admin
from django.urls import path
from App.views import home, login, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", login, name="login"),
    path("register/", register, name="register"),
    path("home/", home, name="home"),
]
