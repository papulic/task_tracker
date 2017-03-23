from django.contrib import admin

from .models import Note, Project

class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ["user", "project"]
    list_filter = ['user']
    list_display_links = ["project"]

    class Meta:
        model = Note


class NoteModelAdmin(admin.ModelAdmin):
    list_display = ["project", "task", "group"]
    list_filter = ['project']

    class Meta:
        model = Note

admin.site.register(Project, ProjectModelAdmin)
admin.site.register(Note, NoteModelAdmin)
