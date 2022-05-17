from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.serializers import ValidationError

from apiv1.serializers.progress_serializers import ProgressSerializer
from progress.models import Progress


class TestProgressSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')

    # serialize
    def test_serialize_progress_correctly(self):
        progress = Progress(user=self.user, language='python',
                            pos='noun', mistake=True, index=100, correct_answer_counter=10)
        serializer = ProgressSerializer(instance=progress)
        self.assertEqual(serializer.data['user'], self.user.id)
        self.assertEqual(serializer.data['language'], 'python')
        self.assertEqual(serializer.data['pos'], 'noun')
        self.assertTrue(serializer.data['mistake'])
        self.assertEqual(serializer.data['index'], 100)
        self.assertEqual(serializer.data['correct_answer_counter'], 10)

    # deserialize
    def test_deserialize_progress_correctly(self):
        data = {
            'user': self.user.id,
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        serializer = ProgressSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    # validatoin test
    def test_validate_language_field(self):
        data = {
            'user': self.user.id,
            'language': 'FORTRAN',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        serializer = ProgressSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('language' in serializer.errors.keys())

    def test_validate_pos_field(self):
        data = {
            'user': self.user.id,
            'language': 'python',
            'pos': 'article',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        serializer = ProgressSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('pos' in serializer.errors.keys())

    def test_unique_constraint(self):
        data = {
            'user': self.user.id,
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        s1 = ProgressSerializer(data=data)
        s1.is_valid(raise_exception=True)
        s1.save()
        s2 = ProgressSerializer(data=data)
        with self.assertRaises(ValidationError):
            s2.is_valid(raise_exception=True)
