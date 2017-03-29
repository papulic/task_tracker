from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission, User


class Project(models.Model):
    user = models.ForeignKey(User, default=1)
    project = models.CharField(max_length=50)
    def __str__(self):
        return self.project

    

team = (
    ('firmware', 'Firmware'),
    ('sqa', 'SQA'),
)
tag = (
    ('backlog', 'BACKLOG'),
    ('preparing', 'PREPARING'),
    ('implement', 'IMPLEMENT'),
    ('testing', 'TESTING'),
    ('done', 'DONE'),
)
    

class Note(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    group = models.CharField(max_length=10,choices=team)
    description = models.CharField(max_length=250)
    tags = models.CharField(max_length=10,choices=tag)
    
    def __str__(self):
        return self.group + ' - ' + self.task
