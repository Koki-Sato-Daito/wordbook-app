from .models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


class UserModelTests(TestCase):
    def test_can_create_a_user_accurately(self):
        User.objects.create_user(
            login_id= 'testuser01',
            password='password'
        )
        user = User.objects.get()
        self.assertEqual('testuser01', user.login_id)
        self.assertFalse(user.is_admin)

    def test_can_create_a_superuser_accurately(self):
        User.objects.create_superuser(
            login_id= 'testuser01',
            password='password'
        )
        user = User.objects.get()
        self.assertEqual('testuser01', user.login_id)
        self.assertTrue(user.is_admin)

    def test_cannot_create_users_with_too_long_login_id(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                login_id= 'n'*21,
                password='password'
            )
    
    def test_cannot_create_users_when_login_id_is_empty(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                login_id= '',
                password='password'
            )

    def test_cannot_create_users_when_login_id_is_duplicated(self):
        User.objects.create_user(
            login_id='abc123',
            password='password'
        )
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                login_id= 'abc123',
                password='password'
            )

    def test_cannot_create_users_with_loginid_including_invalid_char(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                login_id='漢字が含まれる名前',
                password='password'
            )