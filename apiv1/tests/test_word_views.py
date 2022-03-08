import json

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from wordbook.models import Word


class TestMistakeWordAPIView(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = ''
    user = None
    token = None
    word = word1 = word2 = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        cls.TARGET_URL = '/api/v1/users/{user_id}/mistake/'.format(
            user_id=cls.user.id)
        cls.word = cls.word1 = Word.objects.get(pk=1)
        cls.word2 = Word.objects.get(pk=2)

    # post
    def test_user_register_mistske_words_correctly(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistakes": {1, 2, 3}
        }
        response = self.client.post(
            self.TARGET_URL, params)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(len(data['words']), 3)

    def test_return_401_if_without_login(self):
        params = {
            "mistakes": {1, 2, 3}
        }
        response = self.client.post(
            self.TARGET_URL, params)
        self.assertEqual(response.status_code, 401)

    def test_user_register_mistake_words_correctly(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistakes": {1, 2, 3}
        }
        response = self.client.post(
            self.TARGET_URL, params)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(len(data['words']), 3)

    def test_user_cannot_register_with_invalid_params(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistakes": {10000}
        }
        response = self.client.post(
            self.TARGET_URL, params)
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_with_invalid_auth_token(self):
        user2 = get_user_model().objects.get(username='test2')
        token = Token.objects.create(user=user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistakes": {1}
        }
        response = self.client.post(
            self.TARGET_URL, params)
        self.assertEqual(response.status_code, 403)

    # update
    def test_user_remove_mistake_simple_word_correctly(self):
        self.user.mistake_words.add(self.word1, self.word2)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistakes": {1}
        }
        response = self.client.patch(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['words']), 1)
        self.assertEqual(response.data['words'][0]['id'], 2)

    def test_user_remove_mistake_mutiple_words_correctly(self):
        self.user.mistake_words.add(self.word1, self.word2)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistakes": {1,2}
        }
        response = self.client.patch(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['words']), 0)

    def test_should_return_error_when_invalid_params(self):
        self.user.mistake_words.add(self.word1, self.word2)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistakes": {1000000}
        }
        response = self.client.patch(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 400)

    def test_cannot_update_with_invalid_auth_token(self):
        user2 = get_user_model().objects.get(username='test2')
        token = Token.objects.create(user=user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistakes": {1}
        }
        response = self.client.patch(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 403)

    # delete
    def test_user_delete_mistake_words_correctly(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(self.TARGET_URL)
        self.assertEqual(response.status_code, 204)

    def test_return_401_if_without_login(self):
        response = self.client.delete(self.TARGET_URL)
        self.assertEqual(response.status_code, 401)

    def test_cannot_delete_with_invalid_auth_token(self):
        user2 = get_user_model().objects.get(username='test2')
        token = Token.objects.create(user=user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(self.TARGET_URL)
        self.assertEqual(response.status_code, 403)
