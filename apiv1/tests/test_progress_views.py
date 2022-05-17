from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from progress.models import Progress


class TestProgressViewSet(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = '/api/v1/progress/'
    user = None
    progress = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        cls.progress = Progress.objects.create(
            user=cls.user, language='python', pos='noun', mistake=False, index=100, correctAnswerCounter=10)

    # create
    def test_create_progress_insatnce(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            'user': self.user.id,
            'language': 'java',
            'pos': 'verb',
            'mistake': False,
            'index': 100,
            'correctAnswerCounter': 10
        }
        response = self.client.post(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')

    def test_cannot_create_progress_insatnce_with_invalid_data(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            'user': self.user.id,
            'language': 'FORTRAN',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correctAnswerCounter': 10
        }
        response = self.client.post(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('language' in response.data)

    def test_unique_constraint_with_already_exists_params(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        params = {
            'user': self.user.id,
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correctAnswerCounter': 10
        }
        response = self.client.post(self.TARGET_URL, params)
        response = self.client.post(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 400)
        error_msg = response.data['non_field_errors'][0].__str__()
        self.assertTrue(error_msg.startswith('すでに進捗データが存在します。'))

    def test_cannot_create_instance_user_is_not_owner(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        user2 = get_user_model().objects.get(username='test2')
        params = {
            'user': user2.id,
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correctAnswerCounter': 10
        }
        response = self.client.post(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 403)


    # delete
    def test_delete_prgress_data(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            self.TARGET_URL + str(self.progress.id) + '/')
        self.assertEqual(response.status_code, 204)

    def test_cannnot_delete_prgress_data_with_invalid_user_token(self):
        user2 = get_user_model().objects.get(username='test2')
        token = Token.objects.create(user=user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            self.TARGET_URL + str(self.progress.id) + '/')
        self.assertEqual(response.status_code, 403)
