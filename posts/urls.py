from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts_page, name="posts"),
    path("edit/<int:pk>/", views.post_edit, name="post_edit"),
    path("delete/<int:pk>/", views.post_delete, name="post_delete"),

    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("attach/<int:post_id>/", views.upload_attachment, name="upload_attachment"),
]