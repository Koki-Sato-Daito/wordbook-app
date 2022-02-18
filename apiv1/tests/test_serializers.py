from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apiv1 import serializers
from wordbook.models import Word


class TestWordSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    FIXTIRED_WORD_LENGTH = 6

    # testing deserialize
    def test_deserialize_simple_word(self):
        serializer = serializers.WordSerializer(
            instance=Word.objects.get(pk=1))
        self.assertEqual(serializer.data['wordname'], 'apple')

    def test_deserialize_list_words(self):
        serializer = serializers.WordSerializer(
            instance=Word.objects.all(), many=True)
        self.assertEqual(len(serializer.data), self.FIXTIRED_WORD_LENGTH)

    def test_deserialize_users_data(self):
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

    # testing deserialize
    def test_deserialize_users_mistake_words_correctly(self):
        serializer = serializers.UserMistakeSerializer(instance=self.user)
        self.assertEqual(serializer.data['id'], str(self.user.id))

    # testing create
    def test_serialize_mistake_words_correctly(self):
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

    def test_deserialize(self):
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
