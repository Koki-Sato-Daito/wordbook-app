from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from ..models import Progress


class ProgressTestCase(TestCase):
    fixtures = ['users.json', 'words.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')

    def test_create_instance_correctly(self):
        progress = Progress(user=self.user,
                            language='python', pos='noun', mistake=True, index=100, correct_answer_counter=10)
        progress.save()
        self.assertEqual(Progress.objects.all().count(), 1)

    def test_cannnot_create_same_params(self):
        p1 = Progress(user=self.user,
                      language='python', pos='noun', mistake=True, index=100, correct_answer_counter=10)
        p2 = Progress(user=self.user,
                      language='python', pos='noun', mistake=True, index=20, correct_answer_counter=10)
        p1.save()
        with self.assertRaises(IntegrityError):
            p2.save()

    def test_can_create_same_user_different_language(self):
        p1 = Progress(user=self.user,
                      language='python', pos='noun', mistake=True, index=100, correct_answer_counter=10)
        p2 = Progress(user=self.user,
                      language='java', pos='noun', mistake=True, index=300, correct_answer_counter=10)
        p1.save()
        p2.save()

    def test_can_create_same_user_different_mistake_param(self):
        p1 = Progress(user=self.user,
                      language='python', pos='noun', mistake=True, index=100, correct_answer_counter=10)
        p2 = Progress(user=self.user,
                      language='python', pos='noun', mistake=False, index=300, correct_answer_counter=10)
        p1.save()
        p2.save()
