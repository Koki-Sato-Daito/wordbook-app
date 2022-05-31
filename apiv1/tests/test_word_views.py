import json

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from wordbook.models import Word


class TestMistakeWordsViewSet(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = ''
    user = None
    token = None
    word = word1 = word2 = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        cls.TARGET_URL = '/api/v1/mistake_words/'
        cls.word = cls.word1 = Word.objects.get(pk=1)
        cls.word2 = Word.objects.get(pk=2)

    # createメソッド
    def test_create_methods_response_is_correct(self):
        """レスポンスに対するテスト
        """
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistake_words": {1, 2, 3}
        }

        response = self.client.post(self.TARGET_URL, params)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')


    def test_return_401_if_without_login(self):
        """未認証ユーザのリクエストに対するテスト
        """
        params = {
            "mistakes": {1, 2, 3}
        }

        response = self.client.post(self.TARGET_URL, params)
        
        self.assertEqual(response.status_code, 401)


    def test_register_mistake_words_correctly(self):
        """正しくデータが作成されているかのテスト
        """
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistake_words": {1, 2, 3}
        }

        self.client.post(self.TARGET_URL, params)

        self.assertEqual(len(self.user.mistake_words.all()), 3)


    def test_cannot_register_with_invalid_params(self):
        """不正なwordのID値についてテスト
        """
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "mistake_words": {10000}
        }

        response = self.client.post(self.TARGET_URL, params)

        self.assertEqual(response.status_code, 400)


    # destroyメソッド
    def test_delete_methods_response_is_correct(self):
        """レスポンスに対するテスト
        """
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.delete(self.TARGET_URL)

        self.assertEqual(response.status_code, 204)


    def test_delete_all_mistake_words(self):
        """正しくデータが削除されているかのテスト
        """
        mistakes = [1, 2]
        self.user.mistake_words.add(*mistakes)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        self.client.delete(self.TARGET_URL)

        self.assertEqual(len(self.user.mistake_words.all()), 0)


class TestCorrectWordsViewSet(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = ''
    user = None
    token = None
    word = word1 = word2 = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        cls.TARGET_URL = '/api/v1/correct_words/'
        cls.word = cls.word1 = Word.objects.get(pk=1)
        cls.word2 = Word.objects.get(pk=2)

    # createメソッド
    def test_response_is_correct(self):
        """レスポンスに対するテスト
        """
        mistakes = [1, 2]
        self.user.mistake_words.add(*mistakes)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "correct_words": {1}
        }

        response = self.client.post(self.TARGET_URL, params)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')


    def test_remove_only_one_mistake_word_correctly(self):
        """正解データが一つだけの時に正しく登録されるかテスト
        """
        mistakes = [1, 2]
        self.user.mistake_words.add(*mistakes)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "correct_words": {1}
        }

        self.client.post(self.TARGET_URL, params)

        self.assertEqual(len(self.user.mistake_words.all()), 1)
        self.assertEqual(self.user.mistake_words.all()[0].id, 2)


    def test_remove_multiple_mistake_words_correctly(self):
        """正解データが複数あるときに正しく登録されるかテスト
        """
        mistakes = [1, 2]
        self.user.mistake_words.add(*mistakes)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            "correct_words": {1,2}
        }

        self.client.post(self.TARGET_URL, params)

        self.assertEqual(len(self.user.mistake_words.all()), 0)
