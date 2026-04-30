from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts_page, name='posts'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]

