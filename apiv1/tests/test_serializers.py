from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.serializers import ValidationError

from apiv1 import serializers
from wordbook.models import Word
from progress.models import Progress


class TestWordSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    FIXTIRED_WORD_LENGTH = 6

    # testing serialize
    def test_serialize_simple_word(self):
        serializer = serializers.WordSerializer(
            instance=Word.objects.get(pk=1))
        self.assertEqual(serializer.data['wordname'], 'apple')

    def test_serialize_list_words(self):
        serializer = serializers.WordSerializer(
            instance=Word.objects.all(), many=True)
        self.assertEqual(len(serializer.data), self.FIXTIRED_WORD_LENGTH)

    def test_serialize_users_data(self):
        for i in range(1, 3):
            get_user_model().objects.get(
                username=f'test{i}').mistake_words.add(1)
        serializer = serializers.WordSerializer(
            instance=Word.objects.get(pk=1))
        self.assertEqual(len(serializer.data['users']), 2)


class TestUserMistakeSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    user = None
    word = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')
        cls.word = cls.word1 = Word.objects.get(pk=1)
        cls.word2 = Word.objects.get(pk=2)

    # testing serialize
    def test_serialize_users_mistake_words_correctly(self):
        serializer = serializers.UserMistakeSerializer(instance=self.user)
        self.assertEqual(serializer.data['id'], str(self.user.id))

    # testing create
    def test_deserialize_mistake_words_correctly(self):
        data = {
            "mistakes": [self.word.id],
        }
        serializer = serializers.UserMistakeSerializer(
            data=data, context={'user_id': self.user.id})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(len(serializer.data['words']), 1)

    def test_create_method_function_is_not_replacement_but_adding(self):
        data = {
            "mistakes": [self.word1.id],
        }
        serializer = serializers.UserMistakeSerializer(
            data=data, context={'user_id': self.user.id})
        serializer.is_valid()
        serializer.save()
        data = {
            "mistakes": [self.word2.id],
        }
        serializer = serializers.UserMistakeSerializer(
            data=data, context={'user_id': self.user.id})
        serializer.is_valid()
        serializer.save()
        self.assertEqual(len(serializer.data['words']), 2)


class TestTokenSerializer(APITestCase):
    fixtures = ['users.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')

    def test_serialize(self):
        token = Token('abcdefg')
        user_data = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        serializer = serializers.TokenSerializer(
            token, context={'user': user_data})
        self.assertEqual(serializer.data['auth_token'], token.key)
        self.assertEqual(serializer.data['user']['id'], self.user.id)


class TestProgressSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')

    # serialize
    def test_serialize_progress_correctly(self):
        progress = Progress(user=self.user, language='python', pos='noun', mistake=True, index=100)
        serializer = serializers.ProgressSerializer(instance=progress)
        self.assertEqual(serializer.data['user'], self.user.id)
        self.assertEqual(serializer.data['language'], 'python')
        self.assertEqual(serializer.data['pos'], 'noun')
        self.assertTrue(serializer.data['mistake'])
        self.assertEqual(serializer.data['index'], 100)

    # deserialize
    def test_deserialize_progress_correctly(self):
        data = {
            'user': self.user.id,
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
        }
        serializer = serializers.ProgressSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    # validatoin test
    def test_validate_language_field(self):
        data = {
            'user': self.user.id,
            'language': 'FORTRAN',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
        }
        serializer = serializers.ProgressSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('language' in serializer.errors.keys())

    def test_validate_pos_field(self):
        data = {
            'user': self.user.id,
            'language': 'python',
            'pos': 'article',
            'mistake': False,
            'index': 100,
        }
        serializer = serializers.ProgressSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('pos' in serializer.errors.keys())

    def test_unique_constraint(self):
        data = {
            'user': self.user.id,
            'language': 'python',
            'pos': 'noun',
            'mistake': False,
            'index': 100,
        }
        s1 = serializers.ProgressSerializer(data=data)
        s1.is_valid(raise_exception=True)
        s1.save()
        s2 = serializers.ProgressSerializer(data=data)
        with self.assertRaises(ValidationError):
            s2.is_valid(raise_exception=True)


class TestInitWordbookPageSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')
        Progress.objects.create(user=cls.user, language='java', pos='noun', mistake=False, index=100)

    def test_serialize_progress_correctly(self):
        words = Word.objects.filter(language='java', pos='noun')
        progress = Progress.objects.get(user=self.user)
        instance = {'words': words, 'progress': progress}
        serializer = serializers.InitWordbookPageSerializer(instance=instance)
        self.assertEqual(len(serializer.data['words']), 3)
        self.assertEqual(serializer.data['progress']['index'], 100)
