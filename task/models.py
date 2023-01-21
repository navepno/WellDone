
from django.db import models
from django.conf import settings
from django.utils import timezone


class Tag(models.Model):
    tag = models.CharField(max_length=256)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag


class Task(models.Model):
    task = models.CharField(max_length=256)
    content = models.TextField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    solved_status = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag, blank=True)
    # tag = models.ManyToManyField(Tag, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task

