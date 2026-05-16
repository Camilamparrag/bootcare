from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("follow/<int:user_id>/", views.follow_toggle, name="follow-toggle"),
    path("search/", views.user_search, name="user-search"),
]
