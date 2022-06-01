from multiprocessing import context
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

    # シリアライズ　オブジェクト→辞書(レスポンス)
    def test_serialize_progress_correctly(self):
        progress = Progress(user=self.user, language='python',
                            pos='noun', mistake=True, index=100, correct_answer_counter=10)
        serializer = ProgressSerializer(progress)
        self.assertEqual(serializer.data['user'], self.user.id)
        self.assertEqual(serializer.data['language'], 'python')
        self.assertEqual(serializer.data['pos'], 'noun')
        self.assertTrue(serializer.data['mistake'])
        self.assertEqual(serializer.data['index'], 100)
        self.assertEqual(serializer.data['correct_answer_counter'], 10)

    # デシリアライズ　辞書→オブジェクト(リクエスト)
    def test_deserialize_progress_correctly(self):
        data = {
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        serializer = ProgressSerializer(data=data, context={'user': self.user})
        self.assertTrue(serializer.is_valid())

    # フィールド検証テスト
    def test_invalid_language_field(self):
        data = {
            'language': 'FORTRAN',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        serializer = ProgressSerializer(data=data, context={'user': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertTrue('language' in serializer.errors.keys())

    def test_invalid_pos_field(self):
        data = {
            'language': 'python',
            'pos': 'article',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        serializer = ProgressSerializer(data=data, context={'user': self.user})
        self.assertFalse(serializer.is_valid())
        self.assertTrue('pos' in serializer.errors.keys())

    # 複数フィールドに対する検証テスト
    def test_unique_constraint(self):
        data = {
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        Progress.objects.create(user=self.user, **data)
        serializer = ProgressSerializer(data=data, context={'user': self.user})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    # createメソッドに対するテスト
    def test_create_method_can_add_record(self):
        data = {
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
            'correct_answer_counter': 10
        }
        serializer = ProgressSerializer(data=data, context={'user': self.user})
        serializer.is_valid()
        serializer.save()

        progress = Progress.objects.get(language='python', pos='noun')
        self.assertEqual(progress.user, self.user)
