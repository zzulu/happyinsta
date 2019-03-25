from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:post_id>/like/', views.post_like, name='like'),
    path('<int:post_id>/comments/new', views.comment_create, name='comment_create'),
    path('<int:post_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
