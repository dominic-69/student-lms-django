from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Course, Enrollment, Note


class ViewNoteTestCase(TestCase):

    def setUp(self):
 
        # createfake   user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        #login fake user
        self.client.login(
            username='testuser',
            password='testpass123'
        )

        #create course
        self.course = Course.objects.create(
            title='Science',
            description='Science course'
        )

        #enrolll user
        Enrollment.objects.create(
            student=self.user,
            course=self.course
        )

        # create note
        self.note = Note.objects.create(
            student=self.user,
            course=self.course,
            title='My Science Note',
            content='This is my science note'
        )

    def test_view_note_success(self):
        """
        Test that logged-in user can view his own note
        """

        url = reverse('view_note', args=[self.note.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Science Note')
        self.assertContains(response, 'This is my science note')

    def test_view_note_other_user_forbidden(self):
        """
        Test that another user CANNOT view this note
        """

        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

        self.client.login(
            username='otheruser',
            password='otherpass123'
        )

        url = reverse('view_note', args=[self.note.id])
        response = self.client.get(url)

        # for block this using get_object_or_404 
        self.assertEqual(response.status_code, 404)
