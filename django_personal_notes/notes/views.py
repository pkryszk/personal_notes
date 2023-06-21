from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Note


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(notes_list)
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'notes/index.html', context)



def notes_list(request):
    notes = Note.objects.all()
    user = request.user
    context = {
        'notes': notes,
        'user' : user
    }
    return render(request, 'notes/notes_list.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Note

def note_details(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    context = {
        'note': note
    }
    return render(request, 'notes/note_details.html', context)


def test_1(request):
    return HttpResponse(" rendered by test_1")