from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AnonymousConfession, AnonymousComment
from .forms import ConfessionForm, AnonymousCommentForm


@login_required
def confession_list(request):
    confessions = AnonymousConfession.objects.all().prefetch_related("likes", "comments")
    form = ConfessionForm()
    comment_form = AnonymousCommentForm()
    return render(request, "confessions/list.html", {
        "confessions": confessions,
        "form": form,
        "comment_form": comment_form,
    })


@login_required
def confession_create(request):
    if request.method == "POST":
        form = ConfessionForm(request.POST)
        if form.is_valid():
            confession = form.save(commit=False)
            confession.user = request.user
            confession.save()
            messages.success(request, "Confesión publicada anónimamente.")
            return redirect("confessions:list")
    return redirect("confessions:list")


@login_required
def confession_like(request, pk):
    confession = get_object_or_404(AnonymousConfession, pk=pk)
    if confession.likes.filter(id=request.user.id).exists():
        confession.likes.remove(request.user)
    else:
        confession.likes.add(request.user)
    return redirect("confessions:list")


@login_required
def confession_comment(request, pk):
    confession = get_object_or_404(AnonymousConfession, pk=pk)
    if request.method == "POST":
        form = AnonymousCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.confession = confession
            comment.save()
    return redirect("confessions:list")
