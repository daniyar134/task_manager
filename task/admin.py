from django.contrib import admin

from task.models import Task, Description, Comment, Project


admin.site.register(Task)
admin.site.register(Description)
admin.site.register(Comment)
admin.site.register(Project)