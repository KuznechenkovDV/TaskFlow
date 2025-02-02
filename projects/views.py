from channels.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task, Comment, Profile, TaskFile
from django import forms
from .forms import (ProjectForm, TaskForm, TaskStatusForm, CommentForm, UserRegistrationForm, ProfileForm,
                    UserUpdateForm, TaskFileForm)
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
import json
from django.utils.timezone import localtime
from django.contrib.auth.views import LogoutView, PasswordResetView, LoginView
from django.contrib.auth.models import User


def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

def is_manager(user):
    return hasattr(user, 'profile') and user.profile.role == 'manager'

def is_executor(user):
    return hasattr(user, 'profile') and user.profile.role == 'executor'


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "Logged in successfully!")
        return super().form_valid(form)

@login_required
def project_list(request):
    query = request.GET.get('q')
    sort = request.GET.get('sort', 'title')
    if is_admin(request.user):
        projects = Project.objects.all()
    elif is_manager(request.user):
        projects = Project.objects.filter(manager=request.user)
    elif is_executor(request.user):
        projects = Project.objects.filter(tasks__executor=request.user).distinct()
    else:
        projects = Project.objects.none()

    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    projects = projects.order_by(sort)
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if is_admin(request.user):
        pass
    elif is_manager(request.user):
        if project.manager != request.user:
            return HttpResponseForbidden("You do not have permission to view this project.")
    elif is_executor(request.user):
        if not project.tasks.filter(executor=request.user).exists():
            return HttpResponseForbidden("You do not have permission to view this project.")
    else:
        return HttpResponseForbidden("Access denied.")

    query = request.GET.get('q')
    sort = request.GET.get('sort', 'priority')

    if is_executor(request.user):
        tasks = project.tasks.filter(executor=request.user)
    else:
        tasks = project.tasks.all()

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    tasks = tasks.order_by(sort)
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if is_admin(request.user):
        pass
    elif is_manager(request.user):
        if task.project.manager != request.user:
            return HttpResponseForbidden("You do not have permission to view this task.")
    elif is_executor(request.user):
        if task.executor != request.user:
            return HttpResponseForbidden("You do not have permission to view this task.")
    else:
        return HttpResponseForbidden("Access denied.")

    comments = task.comments.all()
    files = task.files.all()
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        data = json.loads(request.body)

        if data.get('action') == 'add':
            comment = Comment.objects.create(
                task=task,
                user=request.user,
                text=data.get('text')
            )
            return JsonResponse({
                'success': True,
                'comment_id': comment.pk,
                'text': comment.text,
                'username': comment.user.username,
                'created_at': localtime(comment.created_at).isoformat()
            })

        elif data.get('action') == 'edit':
            comment = get_object_or_404(Comment, pk=data.get('comment_id'), user=request.user)
            comment.text = data.get('text')
            comment.save()
            return JsonResponse({'success': True})

        elif data.get('action') == 'delete':
            comment = get_object_or_404(Comment, pk=data.get('comment_id'), user=request.user)
            comment.delete()
            return JsonResponse({'success': True})

    form = CommentForm()
    return render(request, 'projects/task_detail.html', {
        'task': task,
        'comments': comments,
        'form': form,
        'files': files
    })

@login_required
def project_form(request, pk=None):
    if pk:
        project = get_object_or_404(Project, pk=pk)
        if not (is_admin(request.user) or (is_manager(request.user) and project.manager == request.user)):
            return HttpResponseForbidden("You do not have permission to edit this project.")
    else:
        project = None

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if is_admin(request.user):
            form.fields['manager'] = forms.ModelChoiceField(
                queryset=User.objects.all()
            )
        if form.is_valid():
            project_instance = form.save(commit=False)
            if is_admin(request.user):
                project_instance.manager = form.cleaned_data.get('manager')
            elif is_manager(request.user):
                project_instance.manager = request.user
            project_instance.save()
            messages.success(request, "Project saved successfully!")
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
        if is_admin(request.user):
            form.fields['manager'] = forms.ModelChoiceField(
                queryset=User.objects.all(),
                initial=project.manager if project else None
            )
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
def task_form(request, pk=None):
    if pk:
        task = get_object_or_404(Task, pk=pk)
        if is_admin(request.user):
            pass
        elif is_manager(request.user):
            if task.project.manager != request.user:
                return HttpResponseForbidden("You do not have permission to edit this task.")
        elif is_executor(request.user):
            if task.executor != request.user:
                return HttpResponseForbidden("You do not have permission to update this task.")
            if request.method == 'POST':
                form = TaskStatusForm(request.POST, instance=task)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Task status updated successfully!")
                    return redirect('project_detail', pk=task.project.pk)
            else:
                form = TaskStatusForm(instance=task)
            return render(request, 'projects/task_form.html', {'form': form})
    else:
        task = None

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task_instance = form.save(commit=False)
            if is_manager(request.user):
                if task_instance.project.manager != request.user:
                    return HttpResponseForbidden("You can only add tasks to projects assigned to you.")
            task_instance.save()
            messages.success(request, "Task saved successfully!")
            return redirect('project_detail', pk=task_instance.project.pk)
    else:
        form = TaskForm(instance=task)
        if is_manager(request.user):
            form.fields['project'].queryset = Project.objects.filter(manager=request.user)
    return render(request, 'projects/task_form.html', {'form': form})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if is_admin(request.user):
        pass
    elif is_manager(request.user):
        if project.manager != request.user:
            return HttpResponseForbidden("You do not have permission to delete this project.")
    else:
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект успешно удалён!')
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if is_admin(request.user):
        pass
    elif is_manager(request.user):
        if task.project.manager != request.user:
            return HttpResponseForbidden("You do not have permission to delete this task.")
    elif is_executor(request.user):
        return HttpResponseForbidden("Executors are not allowed to delete tasks.")
    else:
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена!')
        return redirect('project_detail', pk=task.project.pk)
    return render(request, 'projects/task_confirm_delete.html', {'task': task})


def index(request):
    return render(request, 'index.html')

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

    def logout_and_redirect(self, request):
        logout(request)
        request.session.flush()
        messages.info(request, "You have been logged out successfully.")
        return redirect('login')

    def get(self, request):
        return self.logout_and_redirect(request)

    def post(self, request):
        return self.logout_and_redirect(request)

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        messages.success(self.request, 'Password reset link has been sent to your email.')
        return redirect('login')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            request.session['new_user'] = new_user.username
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('register_done')
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def register_done(request):
    new_user = request.session.pop('new_user', None)
    return render(request, 'account/register_done.html', {'new_user': new_user})


@login_required
def profile(request):
    user = request.user
    role = user.profile.role

    if role == 'manager':
        projects = Project.objects.filter(manager=user)
        tasks = Task.objects.filter(project__manager=user)
    elif role == 'executor':
        projects = Project.objects.filter(tasks__executor=user).distinct()
        tasks = Task.objects.filter(executor=user)
    elif role == 'admin':
        projects = Project.objects.all()
        tasks = Task.objects.all()
    else:
        projects = Project.objects.none()
        tasks = Task.objects.none()

    context = {
        'user': user,
        'role': user.profile.get_role_display(),
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, 'account/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'account/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def upload_task_file(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if is_admin(request.user):
        pass
    elif is_manager(request.user):
        if task.project.manager != request.user:
            return HttpResponseForbidden("You do not have permission to upload file to this task.")
    elif is_executor(request.user):
        if task.executor != request.user:
            return HttpResponseForbidden("You do not have permission to upload file to this task.")
    else:
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        form = TaskFileForm(request.POST, request.FILES)
        if form.is_valid():
            task_file = form.save(commit=False)
            task_file.task = task
            task_file.save()
            messages.success(request, "File uploaded successfully!")
            return redirect('task_detail', pk=pk)
        else:
            messages.error(request, "Error uploading file.")
    else:
        form = TaskFileForm()
    return render(request, 'projects/upload_task_file.html', {'form': form, 'task': task})