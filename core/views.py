from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect("feed")
    return render(request, "core/landing.html")
