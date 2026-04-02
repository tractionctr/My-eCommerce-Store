from django.test import TestCase
from .models import Note
from django.urls import reverse


class NoteTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title="Test Note",
                                        content="Test content")

    def test_note_creation(self):
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "Test content")

    def test_note_list_view(self):
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")

    def test_note_create_view(self):
        response = self.client.post(reverse('note_create'), {
            'title': 'New Note',
            'content': 'New content'
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertEqual(Note.objects.last().title, 'New Note')

    def test_note_update_view(self):
        response = self.client.post(reverse('note_update',
                                            args=[self.note.id]), {
            'title': 'Updated',
            'content': 'Updated content'
        })
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated')

    def test_note_delete_view(self):
        response = self.client.post(reverse('note_delete',
                                            args=[self.note.id]))
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
