from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )

    def test_student_list_requires_login(self):
        response = self.client.get(reverse('students:student_list'))

        self.assertRedirects(
            response,
            f"{reverse('students:login')}?next={reverse('students:student_list')}",
        )

    def test_login_redirects_to_student_list(self):
        response = self.client.post(reverse('students:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })

        self.assertRedirects(response, reverse('students:student_list'))

    def test_login_respects_safe_next_url(self):
        add_url = reverse('students:add_student')
        response = self.client.post(
            f"{reverse('students:login')}?next={add_url}",
            {
                'username': 'testuser',
                'password': 'testpass123',
            },
        )

        self.assertRedirects(response, add_url)
