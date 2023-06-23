from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.forms import modelform_factory
from .forms import LoginForm, RegistrationForm
from .models import Note

NoteForm = modelform_factory(Note, exclude=['user'])


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


@login_required(login_url='index')
def notes_list(request):
    query = request.GET.get('q')
    user = request.user
    notes = Note.objects.filter(user=user)

    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
            return redirect('index')

    if query:
        notes = notes.filter(content__icontains=query)

    context = {
        'notes': notes,
        'user': user,
        'query': query
    }
    return render(request, 'notes/notes_list.html', context)


def new_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            form.save()
            return redirect("notes_list")
    else:
        form = NoteForm(initial={'content': 'type your note here ...'})
    return render(request, 'notes/new_note.html', {"form": form})


@login_required(login_url='index')
def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            note.delete()
            return redirect('notes_list')
        else:
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                return redirect('notes_list')
    else:
        form = NoteForm(instance=note)

    context = {
        'form': form,
        'note': note
    }
    return render(request, 'notes/edit_note.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('notes_list')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'notes/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')
