import json

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from wordbook.models import Word


class TestWordListAPIView(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = '/api/v1/words/'
    user = None
    token = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        for i in range(1, 3):
            Word.objects.get(pk=i).mistake_users.add(cls.user)

    def test_get_words(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.TARGET_URL)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 6)

    def test_get_words_with_params_python_verb(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            self.TARGET_URL,  {'language': 'python', 'pos': 'verb'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_get_words_with_parms_python_noun(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            self.TARGET_URL,  {'language': 'python', 'pos': 'noun'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['wordname'], 'apple')

    def test_cannot_get_response_without_auth(self):
        response = self.client.get(self.TARGET_URL)
        self.assertEqual(response.status_code, 401)

    def test_get_words_with_parms_test1_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.TARGET_URL,
                                   {'language': 'java', 'pos': 'noun', 'mistake_users': self.user.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['wordname'], 'apple')
        self.assertEqual(data[1]['wordname'], 'orange')
