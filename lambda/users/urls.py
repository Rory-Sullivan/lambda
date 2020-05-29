from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("<str:username>/", views.UserDetailView.as_view(), name="profile",),
]
