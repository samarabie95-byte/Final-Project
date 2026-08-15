from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/', views.post_task, name='post_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('bid/<int:bid_id>/accept/', views.accept_bid, name='accept_bid'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]