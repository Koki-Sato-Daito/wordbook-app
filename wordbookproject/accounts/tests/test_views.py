from ..models import User
from django.test import TestCase


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
