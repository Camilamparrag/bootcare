from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post
from .forms import PostForm
from comments.models import Comment
from comments.forms import CommentForm


def feed(request):
    if not request.user.is_authenticated:
        return render(request, "core/landing.html")
    following = request.user.following.values_list("id", flat=True)
    posts = Post.objects.filter(
        Q(user__in=following) | Q(user=request.user)
    ).select_related("user").prefetch_related("likes", "comments").order_by("-created_at")
    return render(request, "posts/feed.html", {"posts": posts})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related("user").prefetch_related("comments__user", "likes"),
        pk=pk,
    )
    comment_form = CommentForm()
    return render(request, "posts/detail.html", {"post": post, "comment_form": comment_form})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Publicación creada.")
            return redirect("feed")
    else:
        form = PostForm()
    return render(request, "posts/create.html", {"form": form})


@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("post-detail", pk=pk)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect("post-detail", pk=pk)
