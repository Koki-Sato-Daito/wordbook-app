from ..forms import (
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm,
)
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


class AuthenticationFormTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            login_id='testuser01',
            password='testuser_pass'
        )

    def test_can_authorize_user_when_precise_inputs(self):
        form = AuthenticationForm(data={
            'login_id': 'testuser01',
            'password': 'testuser_pass',
        })
        self.assertTrue(form.is_valid())

    def test_should_raise_error_when_loginid_is_empty(self):
        form = AuthenticationForm(data={
            'login_id': '',
            'password': 'testuser_pass',
        })
        self.assertFalse(form.is_valid())
        self.assertRegex(str(form['login_id'].errors), 'このフィールドは必須です')

    def test_should_raise_error_when_password_is_empty(self):
        form = AuthenticationForm(data={
            'login_id': 'testuser01',
            'password': '',
        })
        self.assertFalse(form.is_valid())
        self.assertRegex(str(form['password'].errors), 'このフィールドは必須です')

    def test_should_raise_error_when_user_does_not_exist(self):
        form = AuthenticationForm(data={
            'login_id': 'not_exist_user',
            'password': 'testuser_pass',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors()[0],
                         form.error_messages['invalid_login'])

    def test_should_raise_error_when_wrong_password(self):
        form = AuthenticationForm(data={
            'login_id': 'testuser01',
            'password': 'wrong_password',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors()[0],
                         form.error_messages['invalid_login'])

    def test_should_raise_error_when_found_user_is_inactive(self):
        user = User.objects.get(login_id='testuser01')
        form = AuthenticationForm(data={
            'login_id': 'testuser01',
            'password': 'testuser_pass',
        })
        user.is_active = False
        user.save()
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors()[0],
                         form.error_messages['inactive'])
