from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, GroupMember


@login_required
def groups_page(request):
    # CREATE GROUP
    if request.method == "POST":
        group = Group.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            owner=request.user
        )

        # auto-join creator as member (CS-style consistency)
        GroupMember.objects.create(
            group=group,
            user=request.user
        )

        return redirect("groups")

    # LIST GROUPS
    groups = Group.objects.all()

    return render(request, "groups/groups.html", {
        "groups": groups
    })


@login_required
def join_group(request, group_id):
    if request.method == "POST":
        group = get_object_or_404(Group, id=group_id)

        # CS-style explicit join table
        GroupMember.objects.get_or_create(
            group=group,
            user=request.user
        )

    return redirect("groups")