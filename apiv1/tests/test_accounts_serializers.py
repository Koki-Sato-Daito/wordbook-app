from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apiv1.serializers.accounts_serializers import TokenSerializer


class TestTokenSerializer(APITestCase):
    fixtures = ['users.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')

    def test_serialize(self):
        token = Token('abcdefg')
        user_data = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        serializer = TokenSerializer(
            token, context={'user': user_data})
        self.assertEqual(serializer.data['auth_token'], token.key)
        self.assertEqual(serializer.data['user']['id'], self.user.id)
