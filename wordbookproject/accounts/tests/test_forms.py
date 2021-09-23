from ..forms import UserChangeForm, UserCreationForm
from ..models import User
from django.test import TestCase


class UserCreationFormTests(TestCase):
    def test_can_register_user_correctly(self):
        params = {
            'login_id': 'testuser01',
            'password1': 'testuser_pass',
            'password2': 'testuser_pass',
        }
        user = User()
        form = UserCreationForm(params, instance=user)
        self.assertTrue(form.is_valid())

    def test_canont_register_when_loginid_is_too_long(self):
        params = {
            'login_id': 'p'*21,
            'password1': 'testuser_pass',
            'password2': 'testuser_pass',
        }
        user = User()
        form = UserCreationForm(params, instance=user)
        self.assertFalse(form.is_valid())


class UserChangeFormTests(TestCase):
    def test_can_update_user_correctly(self):
        user = User.objects.create_user(
            login_id='testuser01',
            password='testuser_pass',
        )
        params = {
            'login_id': 'updated_testuser',
        }
        form = UserChangeForm(params, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual('updated_testuser', user.login_id)

    def test_cannot_update_user_when_login_id_too_long(self):
        user = User.objects.create_user(
            login_id='testuser01',
            password='testuser_pass',
        )
        params = {
            'login_id': 'p'*21,
        }
        form = UserChangeForm(params, instance=user)
        self.assertFalse(form.is_valid())
