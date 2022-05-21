import djoser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.user_data import UserData


class TestTokenSerializer(APITestCase):
    fixtures = ['users.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')

    def test_serialize(self):
        token = Token('abcdefg')
        data = UserData(token, self.user)
        serializer = djoser.serializers.TokenSerializer(data)
        self.assertEqual(serializer.data['auth_token'], token.key)
        self.assertEqual(serializer.data['user']['id'], str(self.user.id))
