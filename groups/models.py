from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_groups"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "group"

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_memberships"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "group_member"
        unique_together = ("group", "user")
