from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('projects/create/', views.project_form, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_form, name='project_edit'),
    path('tasks/create/', views.task_form, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_form, name='task_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
]