from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import UserRegistrationForm


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada. Inicia sesión.")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request, username):
    profile_user = get_object_or_404(
        User.objects.prefetch_related("posts", "followers", "following"),
        username=username,
    )
    is_following = request.user.following.filter(id=profile_user.id).exists()
    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "is_following": is_following,
    })


@login_required
def user_search(request):
    query = request.GET.get("q", "")
    users = User.objects.exclude(id=request.user.id)
    if query:
        users = users.filter(username__icontains=query)
    following_ids = request.user.following.values_list("id", flat=True)
    return render(request, "accounts/search.html", {
        "users": users,
        "query": query,
        "following_ids": list(following_ids),
    })


@login_required
def follow_toggle(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if request.user == target:
        messages.error(request, "No puedes seguirte a ti mismo.")
        return redirect("profile", username=target.username)
    if request.user.following.filter(id=target.id).exists():
        request.user.following.remove(target)
    else:
        request.user.following.add(target)
    return redirect("profile", username=target.username)
