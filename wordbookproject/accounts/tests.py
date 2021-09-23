from .forms import UserChangeForm, UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


class UserModelTests(TestCase):
    def test_can_create_a_user_accurately(self):
        User.objects.create_user(
            login_id='testuser01',
            password='password'
        )
        user = User.objects.get()
        self.assertEqual('testuser01', user.login_id)
        self.assertFalse(user.is_admin)

    def test_can_create_a_superuser_accurately(self):
        User.objects.create_superuser(
            login_id='testuser01',
            password='password'
        )
        user = User.objects.get()
        self.assertEqual('testuser01', user.login_id)
        self.assertTrue(user.is_admin)

    def test_cannot_create_users_with_too_long_login_id(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                login_id='n'*21,
                password='password'
            )

    def test_cannot_create_users_when_login_id_is_empty(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                login_id='',
                password='password'
            )

    def test_cannot_create_users_when_login_id_is_duplicated(self):
        User.objects.create_user(
            login_id='abc123',
            password='password'
        )
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                login_id='abc123',
                password='password'
            )

    def test_cannot_create_users_with_loginid_including_invalid_char(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                login_id='漢字が含まれる名前',
                password='password'
            )


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


class SignUpViewTests(TestCase):
    def test_should_render_template_if_sending_get_request(self):
        response = self.client.get('/accounts/signup/')
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_should_render_title_if_sending_get_request(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, 'サインアップ', status_code=200)

    def test_should_create_user_if_sending_user_data(self):
        self.client.post('/accounts/signup/', {
            'login_id': 'testuser',
            'password1': 'test_pass',
            'password2': 'test_pass',
        })
        self.assertEqual(User.objects.get().login_id, 'testuser')

    def test_should_redirect_top_if_sending_user_data(self):
        response = self.client.post('/accounts/signup/', {
            'login_id': 'testuser',
            'password1': 'test_pass',
            'password2': 'test_pass',
        })
        self.assertRedirects(response, '/')

    # TODO 以降のテスト認証バックエンド実装後に実装する
    def test_should_login_if_sending_user_create(self):
        pass

    def test_should_redirect_if_sending_get_request_with_login_user(self):
        pass
