from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название проекта')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name


class Task(models.Model):
    NEED = 'need'
    PROGRESS = 'progress'
    DONE = 'done'
    REJECTED = 'rejected'
    STATUS_CHOICE = (
        (NEED, 'Требует выполенения'),
        (PROGRESS, 'Выполняется'),
        (DONE, 'Закончено'),
        (REJECTED, 'Отменено')
    )
    name = models.CharField(max_length=255, verbose_name='Название задачи')
    project = models.ForeignKey(Project, null=True, blank=True, verbose_name='Проект')
    status = models.CharField(max_length=15, choices=STATUS_CHOICE, verbose_name='Статус')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='author')
    maker = models.ForeignKey(User, null=True, blank=True, verbose_name='Исполнитель', related_name='maker')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name


class Description(models.Model):
    text = models.TextField(verbose_name='Текст описания')
    task = models.ForeignKey(Task, null=True, blank=True, verbose_name='Задача', related_name='description')

    class Meta:
        verbose_name = 'Описание'
        verbose_name_plural = 'Описания'

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    task = models.ForeignKey(Task, null=True, blank=True, verbose_name='Задача', related_name='comment')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text