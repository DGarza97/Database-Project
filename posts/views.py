from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Post, Like, Comment, PostAttachment, Notification
from .forms import PostForm


# ---------------- FEED ----------------
@login_required
def posts_page(request):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Post.objects.create(
                user=request.user,
                content=content
            )

    posts = Post.objects.all().order_by("-created_at")

    return render(request, "posts/feed.html", {
        "posts": posts
    })


# ---------------- EDIT ----------------
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

            next_url = request.POST.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)

            return redirect("posts")
    else:
        form = PostForm(instance=post)

    return render(request, "posts/editpost.html", {
        "form": form,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "/")),
    })


# ---------------- DELETE ----------------
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("posts")

    return render(request, "posts/deletepost.html", {
        "post": post
    })


# ---------------- LIKE TOGGLE ----------------
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect("posts")


# ---------------- COMMENT ----------------
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        Comment.objects.create(
            user=request.user,
            post=post,
            content=request.POST["content"]
        )

        # notification
        if post.user != request.user:
            Notification.objects.create(
                user=post.user,
                message=f"{request.user.username} commented on your post"
            )

    return redirect("posts")


# ---------------- ATTACHMENT ----------------
@login_required
def upload_attachment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST" and request.FILES.get("file"):
        PostAttachment.objects.create(
            post=post,
            file=request.FILES["file"]
        )

    return redirect("posts")
