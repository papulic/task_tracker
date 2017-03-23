from django.conf.urls import url
from . import views


app_name = 'board'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<project_id>[0-9]+)/$', views.detail, name='notes'),
    url(r'^create_project/$', views.create_project, name='project-add'),
    url(r'^(?P<project_id>[0-9]+)/create_note/$', views.create_note, name='note-add'),
    url(r'^(?P<project_id>[0-9]+)/update/(?P<note_id>[0-9]+)/$', views.note_update, name='note-update'),
    url(r'^(?P<project_id>[0-9]+)/delete/$', views.delete_project, name='project-delete'),
    url(r'^(?P<project_id>[0-9]+)/delete/(?P<note_id>[0-9]+)/$', views.note_delete, name='note-delete'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^password/$', views.change_password, name='change_password'),


]
