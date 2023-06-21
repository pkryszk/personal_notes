from django.urls import path
from .views import index, notes_list,test_1,note_details

urlpatterns = [
    path('', index, name='index'),
    path('1', test_1, name='test_1'),
    path('notes_list', notes_list, name='notes_list'),
    path('notes/<int:note_id>/', note_details, name='note_detail'),
    ]