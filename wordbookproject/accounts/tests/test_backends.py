from django.test import TestCase
from ..models import User

class CustomBackEndTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            login_id='testuser',
            password='testuser_pass'
        )
    def test_can_login(self):
        login = self.client.login(
            login_id='testuser',
            password='testuser_pass')
        self.assertTrue(login)
    
    def test_cannot_login_when_login_id_is_wrong(self):
        login = self.client.login(
            login_id='wrong_user',
            password='testuser_pass'
        )
        self.assertFalse(login)
