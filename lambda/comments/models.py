from django.db import models
from tasks.models import Task
from django.contrib.auth.models import User
from projects.models import Project


class TaskComment(models.Model):

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    assigned_to_task = models.ForeignKey(Task, on_delete=models.PROTECT)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class ProjectComment(models.Model):

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    assigned_to_project = models.ForeignKey(Project, on_delete=models.PROTECT)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)