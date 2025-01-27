from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task
from django.shortcuts import render
from .forms import ProjectForm, TaskForm
from django.contrib import messages
from django.db.models import Q


def project_list(request):
    query = request.GET.get('q')
    sort = request.GET.get('sort', 'title')

    projects = Project.objects.all()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    projects = projects.order_by(sort)

    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    query = request.GET.get('q')
    sort = request.GET.get('sort', 'priority')

    tasks = project.tasks.all()

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    tasks = tasks.order_by(sort)

    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'projects/task_detail.html', {'task': task})


def project_form(request, pk=None):
    if pk:
        project = get_object_or_404(Project, pk=pk)
    else:
        project = None

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {'form': form})


def task_form(request, pk=None):
    if pk:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = None

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'projects/task_form.html', {'form': form})

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект успешно удалён!')
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена!')
        return redirect('project_detail', pk=task.project.pk)
    return render(request, 'projects/task_confirm_delete.html', {'task': task})


def index(request):
    return render(request, 'index.html')