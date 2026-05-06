from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message


@login_required
def inbox_view(request, user_id=None):
    # Get all users you have messaged with (sent or received)
    conversations = User.objects.filter(
        Q(sent_messages__receiver=request.user) |
        Q(received_messages__sender=request.user)
    ).distinct()

    active_user = None
    messages = []

    if user_id:
        active_user = get_object_or_404(User, id=user_id)

        # Fetch direct messages between the two users
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=active_user) |
            Q(sender=active_user, receiver=request.user)
        ).order_by("created_at")

        if request.method == "POST":
            Message.objects.create(
                sender=request.user,
                receiver=active_user,
                content=request.POST["content"]
            )
            return redirect("messages:conversation", user_id=active_user.id)

    return render(request, "messaging/messages.html", {
        "conversations": conversations,
        "active_user": active_user,
        "messages": messages,
    })