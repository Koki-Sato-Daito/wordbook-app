from ..models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


class UserModelTests(TestCase):
    def test_can_create_a_user_accurately(self):
        User.objects.create_user('testuser01', 'test@example.com', 'password')
        user = User.objects.get()
        self.assertEqual('testuser01', user.username)
        self.assertFalse(user.is_staff)

    def test_can_create_a_superuser_accurately(self):
        User.objects.create_superuser('testuser01', 'test@example.com', 'password')
        user = User.objects.get()
        self.assertEqual('testuser01', user.username)
        self.assertTrue(user.is_staff)

    def test_cannot_create_users_with_too_long_username(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user('n'*21, 'test@example.com', 'password')

    def test_cannot_create_user_when_username_is_empty(self):
        with self.assertRaises(ValueError):
            User.objects.create_user('', 'test@example.com', 'password')

    def test_cannot_create_user_when_email_is_duplicated(self):
        User.objects.create_user('testuser01', 'test@example.com', 'password')
        with self.assertRaises(ValidationError):
            User.objects.create_user('testuser02', 'test@example.com', 'password')

    def test_cannot_create_user_with_username_including_invalid_char(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user('(無効な記号)', 'test@example.com', 'password')

    def test_cannot_create_user_with_invalid_email(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user('testuser', 'test.example.com', 'password')
