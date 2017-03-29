from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Project
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm, NoteForm, ProjectForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse




def index(request):
    if not request.user.is_authenticated():
        return render(request, 'board/login.html')
    else:
        projects = Project.objects.filter(user=request.user)
        
        return render(request, 'board/index.html', {
            'projects': projects,
        })


def detail(request, project_id):
    if not request.user.is_authenticated():
        return render(request, 'board/login.html')
    else:
        projects = get_object_or_404(Project, pk=project_id)
        notes = Note.objects.filter(project=project_id)
        return render(request, 'board/notes.html', {
            'projects': projects,
            'project_id': project_id,
            'notes': notes,
        })

def create_project(request):
    if not request.user.is_authenticated():
        return render(request, 'board/login.html')
    else:
        projects = Project.objects.filter(user=request.user)
        form = ProjectForm(request.POST or None)
        projects_list = []
        for i in projects:
            projects_list.append(str(i))
        if request.method == 'POST':
            if form.is_valid():
                project = form.save(commit=False)
                project.user = request.user
                if str(project) in projects_list:
                    messages.success(request, "This project already exists!")
                    return HttpResponseRedirect(reverse('board:index'))
                else:
                    project.save()
                    return HttpResponseRedirect(reverse('board:index'))
        context = {
            "form": form,
            
        }
        return render(request, 'board/project_form.html', context)
        

def create_note(request, project_id):
    form = NoteForm(request.POST or None)
    projects = get_object_or_404(Project, pk=project_id)
    notes = Note.objects.filter(project=project_id)
    notes_list = []
    for i in notes:
        notes_list.append(str(i))
    if request.method == 'POST':
        if form.is_valid():
            note = form.save(commit=False)
            note.project = projects
            if str(note) in notes_list:
                messages.success(request, "This task already exists!")
                return HttpResponseRedirect('/board/{project_id}'.format(project_id=project_id))
            else:
                note.save()
                return HttpResponseRedirect('/board/{project_id}'.format(project_id=project_id))
            # return render(request, 'board/notes.html', {
            #     'projects': projects,
            #     'project_id': project_id,
            #     'notes': notes
            # })
    context = {
        "form": form,
        'projects': projects,
        'project_id': project_id,
        'notes': notes
    }
    return render(request, 'board/note_form.html', context)
    

def note_update(request, project_id, note_id):
    instance = Note.objects.get(pk=note_id)
    projects = get_object_or_404(Project, pk=project_id)
    form = NoteForm(request.POST or None, instance=instance)
    notes = Note.objects.filter(project=project_id)
    if form.is_valid():
        note = form.save(commit=False)
        note.project = projects
        note.save()
        return render(request, 'board/notes.html', {
            'projects': projects,
            'project_id': project_id,
            'note_id': note_id,
            'notes': notes
        })
    context = {
        "form": form,
        'project_id': project_id,
        'note_id': note_id,
    }
    return render(request, 'board/note_update_form.html', context)


def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    projects = Project.objects.filter(user=request.user)

    return render(request, 'board/index.html', {
        'projects': projects,
    })
    
def note_delete(request, project_id, note_id):
    project = get_object_or_404(Project, pk=project_id)
    note = Note.objects.get(pk=note_id)
    note.delete()
    notes = Note.objects.filter(project=project_id)
    return render(request, 'board/notes.html', {"project": project, "notes": notes,
                                                "project_id": project_id})

def delete_all(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    notes = Note.objects.filter(project=project_id)
    for note in notes:
        note.delete()
    notes = Note.objects.filter(project=project_id)
    return render(request, 'board/notes.html', {"project": project, "notes": notes,
                                                "project_id": project_id})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                projects = Project.objects.filter(user=request.user)
                return render(request, 'board/index.html', {'projects': projects})
            else:
                return render(request, 'board/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'board/login.html', {'error_message': 'Invalid login'})
    return render(request, 'board/login.html')
    

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'board/login.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('board:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'board/change_password.html', {
        'form': form
    })

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                projects = Project.objects.filter(user=request.user)
    
                return render(request, 'board/index.html', {
                    'projects': projects,
            })
    context = {
        "form": form,
    }
    return render(request, 'board/register.html', context)
