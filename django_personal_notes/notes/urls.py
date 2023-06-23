from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import index, notes_list,new_note,edit_note,register

urlpatterns = [
    path('', index, name='index'),
    path('notes_list', notes_list, name='notes_list'),
    path('<int:note_id>', edit_note, name='edit_note'),
    path('new_note', new_note, name='new_note'),
    path('register/', register, name='register'),

    ]