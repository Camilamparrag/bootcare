from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("post/<int:pk>/", views.post_detail, name="post-detail"),
    path("post/create/", views.post_create, name="post-create"),
    path("post/<int:pk>/like/", views.like_toggle, name="like-toggle"),
    path("post/<int:pk>/comment/", views.add_comment, name="add-comment"),
]
