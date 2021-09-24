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

    def test_should_keep_login_when_user_create_request(self):
        response = self.client.post('/accounts/signup/', {
            'login_id': 'testuser',
            'password1': 'test_pass',
            'password2': 'test_pass',
        })
        self.assertTrue('sessionid' in response.cookies.keys())
        self.client.logout()
        response = self.client.get('/accounts/signup/')
        self.assertFalse('sessionid' in response.cookies.keys())

    def test_should_reject_when_alraedy_logined(self):
        self.client.force_login(User.objects.create_user(
            login_id='testuser',
            password='test_pass'
        ))
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 403)


class LoginViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            login_id='testuser',
            password='testuser_pass'
        )

    def test_should_render_template_when_sending_get_request(self):
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_should_render_title_when_sending_get_request(self):
        response = self.client.get('/accounts/login/')
        self.assertContains(response, 'ログイン', status_code=200)

    def test_should_redirect_after_successful_login(self):
        response = self.client.post('/accounts/login/', {
            'login_id': 'testuser',
            'password': 'testuser_pass',
        })
        self.assertEqual(response.status_code, 302)

    def test_should_render_loginpage_when_failed_login(self):
        response = self.client.post('/accounts/login/', {
            'login_id': 'testuser',
            'password': 'wrong_pass'
        })
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, '正しいログインIDとパスワードを入力してください。')

    def test_httpredirect_when_already_logined(self):
        self.client.login(login_id='testuser', password='testuser_pass')
        response = self.client.get('/accounts/login/')
        self.assertRedirects(response, '/')
