import json

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from progress.models import Progress


class TestInitWordbookPageAPIView(APITestCase):
    fixtures = ['users.json', 'words.json']
    TARGET_URL = '/api/v1/init_wordbook_page/'
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(email='test1@example.com')
        Progress.objects.create(
            language='java', pos='noun', user=cls.user, mistake=False, index=100, correctAnswerCounter=10)

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
        self.assertEqual(data['progress']['correctAnswerCounter'], 10)

    def test_return_only_words_when_progress_data_is_not_exists(self):
        self.client.force_authenticate(user=self.user)
        # java,noun,mistake=trueはwordsもprogressも存在しない。
        response = self.client.get(
            self.TARGET_URL + '?language=java&pos=noun&mistake=true&user=' + str(self.user.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['words']), 0)
        self.assertEqual(data['progress'], None)

    def test_words_order_is_descending(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            self.TARGET_URL + '?language=java&pos=noun')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['words'][0]['freq'] > data['words'][1]['freq'])
        self.assertTrue(data['words'][1]['freq'] > data['words'][2]['freq'])
