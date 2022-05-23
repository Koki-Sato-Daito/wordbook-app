from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apiv1.serializers.page_serializers import ExamPageSerializer
from apiv1.serializers.page_serializers import ExamPageData
from wordbook.models import Word
from progress.models import Progress


class TestExamPageSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')
        Progress.objects.create(
            user=cls.user, language='java', pos='noun', mistake=False, index=100, correct_answer_counter=10)

    def test_serialize_progress_correctly(self):
        words = Word.objects.filter(language='java', pos='noun')
        progress = Progress.objects.get(user=self.user)
        queryset_dict = {'words': words, 'progress': progress}

        instance = ExamPageData(**queryset_dict)
        serializer = ExamPageSerializer(instance)

        self.assertEqual(len(serializer.data['words']), 3)
        self.assertEqual(serializer.data['progress']['index'], 100)
        self.assertEqual(serializer.data['progress']['correct_answer_counter'], 10)
