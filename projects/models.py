from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершен'),
        ('paused', 'Приостановлен'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус"
    )

    def __str__(self):
        return self.title


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'Высокий'),
        ('medium', 'Средний'),
        ('low', 'Низкий'),
    ]

    # Расширенные статусы
    STATUS_CHOICES = [
        ('not_started', 'Не начата'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершена'),
        ('on_hold', 'На удержании'),       # Новый статус
        ('cancelled', 'Отменена'),        # Новый статус
        ('under_review', 'На проверке'), # Новый статус
    ]

    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Проект"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Приоритет"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='not_started',
        verbose_name="Статус"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")

    def __str__(self):
        return f"{self.title} ({self.project.title})"


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Задача"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.user.username} к задаче {self.task.title}"


class TaskFile(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name="Задача"
    )
    file = models.FileField(upload_to='task_files/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    def __str__(self):
        return f"Файл для задачи {self.task.title}"
