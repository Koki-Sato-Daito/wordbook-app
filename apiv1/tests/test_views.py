import json

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from wordbook.models import Word
from progress.models import Progress


class TestWordListAPIView(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = '/api/v1/words/'
    user = None
    token = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        for i in range(1, 3):
            cls.user.mistake_words.add(Word.objects.get(pk=i).id)

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
                                   {'language': 'java', 'pos': 'noun', 'users': self.user.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['wordname'], 'apple')
        self.assertEqual(data[1]['wordname'], 'orange')


class TestMistakeWordAPIView(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = ''
    user = None
    token = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        cls.TARGET_URL = '/api/v1/users/{user_id}/mistake/'.format(
            user_id=cls.user.id)

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

    # retrieve
    def test_retireve_progress_instance(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.TARGET_URL + str(self.progress.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['index'], self.progress.index)

    def test_cannot_retireve_progress_instance_without_login(self):
        response = self.client.get(self.TARGET_URL + str(self.progress.id) + '/')
        self.assertEqual(response.status_code, 401)

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
        response = self.client.delete(self.TARGET_URL + str(self.progress.id) + '/')
        self.assertEqual(response.status_code, 204)

