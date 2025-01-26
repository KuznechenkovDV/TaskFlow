from django.contrib import admin
from .models import Project, Task, Comment, TaskFile

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'end_date')
    list_filter = ('status',)
    search_fields = ('title', 'description')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'status', 'start_date', 'end_date')
    list_filter = ('priority', 'status', 'project')
    search_fields = ('title', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('text',)

@admin.register(TaskFile)
class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('task', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)

