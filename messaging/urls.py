from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path("", views.inbox_view, name="inbox"),
    path("<int:conversation_id>/", views.inbox_view, name="conversation"),
]
