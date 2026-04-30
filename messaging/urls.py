from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox_view, name="inbox"),
    path("<int:conversation_id>/", views.inbox_view, name="conversation"),
]
