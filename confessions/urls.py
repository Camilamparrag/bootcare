from django.urls import path
from . import views

app_name = "confessions"

urlpatterns = [
    path("", views.confession_list, name="list"),
    path("create/", views.confession_create, name="create"),
    path("<int:pk>/like/", views.confession_like, name="like"),
    path("<int:pk>/comment/", views.confession_comment, name="comment"),
]
