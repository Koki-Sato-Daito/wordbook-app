import json

from django.test import TestCase

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



class WordBookPageTests(TestCase):
    def test_should_render_template_when_sending_get_request(self):
        response = self.client.get('/vocabulary/python/verb')
        self.assertTemplateUsed(response, 'vocabulary/wordbook.html')
    
    def test_should_set_context_data(self):
        response = self.client.get('/vocabulary/python/verb')
        self.assertEqual(response.context['language'], 'python')
        self.assertEqual(response.context['pos_param'], 'verb')

    def test_cannot_access_data_with_invalid_endpoint(self):
        response = self.client.get('/vocabulary/python/invalid_pos')
        self.assertEqual(response.status_code, 403)


class SelectLanguageTests(TestCase):
    def test_should_render_template_when_sending_get_request(self):
        response = self.client.get('/vocabulary/languages')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vocabulary/languages.html')