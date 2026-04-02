from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm


# show all notes
def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/list.html', {'notes': notes})


# create note
def note_create(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('note_list')
    return render(request, 'notes/form.html', {'form': form})


# update note
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('note_list')
    return render(request, 'notes/form.html', {'form': form})


# delete note
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect('note_list')
