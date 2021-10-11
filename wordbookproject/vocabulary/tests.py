import json

from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Vocabulary

class FilteredWordsViewFuncTests(TestCase):
    def setUp(self):
        Vocabulary.objects.create(wordname='study', meaning='勉強する', pos='verb', python_freq=500)
        Vocabulary.objects.create(wordname='walk', meaning='歩く', pos='verb', python_freq=0)
        Vocabulary.objects.create(wordname='very', meaning='とても', pos='adverb', python_freq=500)

    def test_can_return_json_correctly(self):
        response = self.client.get('/vocabulary/data/python/verb')
        self.assertEqual(response.status_code, 200)
        json_content = json.loads(response.content)
        self.assertEqual(len(json_content["data"]), 1)
        self.assertEqual(json_content["data"][0]['wordname'], 'study')

    def test_cannot_access_data_with_invalid_endpoint(self):
        response = self.client.get('/vocabulary/data/non_existence_lang/verb')
        self.assertEqual(response.status_code, 403)

    def test_should_return_json_correctly_with_mistake_params(self):
        User = get_user_model()
        testuser = User.objects.create_user(login_id='testuser', password="testuser_pass")
        self.client.login(login_id='testuser', password='testuser_pass')
        mistake_word = Vocabulary.objects.create(wordname='move', meaning='移動する', pos='verb', python_freq=300)
        mistake_word.mistake_users.add(testuser)

        response = self.client.get('/vocabulary/data/python/verb?mistake=True')
        json_content = json.loads(response.content)
        self.assertEqual(len(json_content["data"]), 1)
        self.assertEqual(json_content["data"][0]['wordname'], 'move')


class WordBookPageTests(TestCase):
    def test_should_render_template_when_sending_get_request(self):
        response = self.client.get('/vocabulary/python/verb')
        self.assertTemplateUsed(response, 'vocabulary/wordbook.html')
    
    def test_should_set_context_data(self):
        response = self.client.get('/vocabulary/python/verb?mistake=True')
        self.assertEqual(response.context['language'], 'python')
        self.assertEqual(response.context['pos_param'], 'verb')
        self.assertEqual(response.context['mistake'], 'True')

    def test_cannot_access_data_with_invalid_endpoint(self):
        response = self.client.get('/vocabulary/python/invalid_pos')
        self.assertEqual(response.status_code, 403)


class SelectLanguageTests(TestCase):
    def test_should_render_template_when_sending_get_request(self):
        response = self.client.get('/vocabulary/languages')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vocabulary/languages.html')


class SaveMistakenWordsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(login_id='testuser', password="testuser_pass")
        self.client.login(login_id='testuser', password='testuser_pass')

        Vocabulary.objects.create(pk=1, wordname='study', meaning='勉強する', pos='verb', python_freq=500)
        Vocabulary.objects.create(pk=2, wordname='walk', meaning='歩く', pos='verb', python_freq=200)
        Vocabulary.objects.create(pk=3, wordname='move', meaning='移動する', pos='verb', python_freq=100)
    
    def test_should_return_statuscord_200(self):
        response = self.client.post('/vocabulary/mistake', 
                         json.dumps({"words": [1]}), content_type='applicaiton/json')
        self.assertEqual(response.status_code, 200)

    def test_can_return_save_mistaken_words_when_relation_already_exist(self):
        self.client.post('/vocabulary/mistake', 
                         json.dumps({"words": [1,3]}), content_type='applicaiton/json')
        self.client.post('/vocabulary/mistake', 
                         json.dumps({"words": [2,3]}), content_type='applicaiton/json')

        User = get_user_model()
        user = User.objects.get(login_id='testuser')

        self.assertEqual(Vocabulary.objects.get(pk=2).mistake_users.first(), user)
        self.assertEqual(Vocabulary.objects.get(pk=3).mistake_users.first(), user)
        self.assertNotEqual(Vocabulary.objects.get(pk=1).mistake_users.first(), user)
        



    