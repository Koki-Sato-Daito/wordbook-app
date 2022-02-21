from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Progress


class ProgressTestCase(TestCase):
    fixtures = ['user.json', 'words.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')

    def test_create_instance_correctly(self):
        progress = Progress(user=self.user,
                            language='python', pos='noun', mistake=True, index=100)
        progress.save()
        self.assertEqual(Progress.objects.all().count(), 1)
