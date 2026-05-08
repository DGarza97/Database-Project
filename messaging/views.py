from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Message


@login_required
def inbox_view(request, user_id=None):

    conversations = User.objects.filter(
        is_superuser=False
    ).exclude(
        id=request.user.id
    )

    active_user = None
    messages = []

    if user_id is not None:

        active_user = get_object_or_404(
            User,
            id=user_id,
            is_superuser=False
        )

        messages = Message.objects.filter(
            Q(sender=request.user, receiver=active_user) |
            Q(sender=active_user, receiver=request.user)
        ).order_by("created_at")

        if request.method == "POST":

            content = request.POST.get("content")

            if content:
                Message.objects.create(
                    sender=request.user,
                    receiver=active_user,
                    content=content
                )

            return redirect(
                "messaging:conversation",
                user_id=active_user.id
            )

    return render(request, "messaging/messages.html", {
        "conversations": conversations,
        "active_user": active_user,
        "messages": messages,
    })