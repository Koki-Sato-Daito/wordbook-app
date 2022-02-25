import json

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from wordbook.models import Word
from progress.models import Progress


class TestInitWordbookPageAPIView(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = '/api/v1/init_wordbook_page/'
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        Progress.objects.create(
            language='java', pos='noun', user=cls.user, mistake=False, index=100)

    def test_cannot_return_data_without_login(self):
        response = self.client.get(self.TARGET_URL + '?language=java&pos=noun')
        self.assertEqual(response.status_code, 401)

    def test_return_words_with_params_language_pos(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.TARGET_URL + '?language=java&pos=noun')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['words']), 3)

    def test_return_words_and_progress(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            self.TARGET_URL + '?language=java&pos=noun&mistake=false&user=' + str(self.user.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['words']), 3)
        self.assertEqual(data['progress']['index'], 100)

    def test_return_only_words_when_progress_data_is_not_exists(self):
        self.client.force_authenticate(user=self.user)
        # java,noun,mistake=trueはwordsもprogressも存在しない。
        response = self.client.get(
            self.TARGET_URL + '?language=java&pos=noun&mistake=true&user=' + str(self.user.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['words']), 0)
        self.assertEqual(data['progress'], None)


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
        self.client.force_authenticate(user=self.user)
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
        self.client.force_authenticate(user=self.user)
        params = {
            "mistakes": {1, 2, 3}
        }
        response = self.client.post(
            self.TARGET_URL, params)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(len(data['words']), 3)

    def test_user_cannot_register_with_invalid_params(self):
        self.client.force_authenticate(user=self.user)
        params = {
            "mistakes": {10000}
        }
        response = self.client.post(
            self.TARGET_URL, params)
        self.assertEqual(response.status_code, 400)

    # update
    def test_user_remove_mistake_simple_word_correctly(self):
        self.user.mistake_words.add(self.word1, self.word2)
        self.client.force_authenticate(user=self.user)
        params = {
            "mistakes": {1}
        }
        response = self.client.patch(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['words']), 1)
        self.assertEqual(response.data['words'][0]['id'], 2)

    def test_user_remove_mistake_mutiple_words_correctly(self):
        self.user.mistake_words.add(self.word1, self.word2)
        self.client.force_authenticate(user=self.user)
        params = {
            "mistakes": {1,2}
        }
        response = self.client.patch(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['words']), 0)

    def test_should_return_error_when_invalid_params(self):
        self.user.mistake_words.add(self.word1, self.word2)
        self.client.force_authenticate(user=self.user)
        params = {
            "mistakes": {1000000}
        }
        response = self.client.patch(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 400)

    # delete
    def test_user_delete_mistake_words_correctly(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.TARGET_URL)
        self.assertEqual(response.status_code, 204)

    def test_return_401_if_without_login(self):
        response = self.client.delete(self.TARGET_URL)
        self.assertEqual(response.status_code, 401)


class TestProgressViewSet(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = '/api/v1/progress/'
    user = None
    progress = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        cls.progress = Progress.objects.create(
            user=cls.user, language='python', pos='noun', mistake=False, index=100)

    # create
    def test_create_progress_insatnce(self):
        self.client.force_authenticate(user=self.user)
        params = {
            'user': self.user.id,
            'language': 'java',
            'pos': 'verb',
            'mistake': False,
            'index': 100
        }
        response = self.client.post(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 201)

    def test_cannot_create_progress_insatnce_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        params = {
            'user': self.user.id,
            'language': 'FORTRAN',
            'pos': 'noun',
            'mistake': False,
            'index': 100
        }
        response = self.client.post(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('language' in response.data)

    def test_unique_constraint_with_already_exists_params(self):
        self.client.force_authenticate(user=self.user)
        params = {
            'user': self.user.id,
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100
        }
        response = self.client.post(self.TARGET_URL, params)
        response = self.client.post(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 400)
        error_msg = response.data['non_field_errors'][0].__str__()
        self.assertTrue(error_msg.startswith('すでに進捗データが存在します。'))

    # delete
    def test_delete_prgress_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            self.TARGET_URL + str(self.progress.id) + '/')
        self.assertEqual(response.status_code, 204)
