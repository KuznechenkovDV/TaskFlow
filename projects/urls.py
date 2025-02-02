from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView, CustomPasswordResetView, CustomLoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_change/', CustomPasswordResetView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', views.register, name='register'),
    path('register/done/', views.register_done, name='register_done'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('projects/create/', views.project_form, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_form, name='project_edit'),
    path('tasks/create/', views.task_form, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_form, name='task_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/upload_file/', views.upload_task_file, name='upload_task_file'),
]