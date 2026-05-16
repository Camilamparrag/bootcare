from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ChatMessage
from accounts.models import User


@login_required
def inbox(request):
    users = User.objects.exclude(id=request.user.id)
    last_messages = []
    for u in users:
        last = ChatMessage.objects.filter(
            Q(sender=request.user, receiver=u) | Q(sender=u, receiver=request.user)
        ).last()
        if last:
            unread = ChatMessage.objects.filter(sender=u, receiver=request.user, is_read=False).count()
            last_messages.append((u, last, unread))
    return render(request, "chat/inbox.html", {"conversations": last_messages})


@login_required
def conversation(request, user_id):
    other = get_object_or_404(User, id=user_id)
    messages_list = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other) | Q(sender=other, receiver=request.user)
    ).select_related("sender", "receiver")
    ChatMessage.objects.filter(sender=other, receiver=request.user, is_read=False).update(is_read=True)
    return render(request, "chat/conversation.html", {
        "other": other,
        "messages": messages_list,
    })


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == "POST":
        text = request.POST.get("message", "").strip()
        if text:
            ChatMessage.objects.create(sender=request.user, receiver=receiver, message=text)
    return redirect("chat:conversation", user_id=receiver_id)
