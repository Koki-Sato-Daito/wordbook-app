from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apiv1.serializers.words_serializers import WordSerializer, UserMistakeSerializer
from wordbook.models import Word


class TestWordSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    FIXTIRED_WORD_LENGTH = 6

    # testing serialize
    def test_serialize_simple_word(self):
        serializer = WordSerializer(
            instance=Word.objects.get(pk=1))
        self.assertEqual(serializer.data['wordname'], 'apple')

    def test_serialize_list_words(self):
        serializer = WordSerializer(
            instance=Word.objects.all(), many=True)
        self.assertEqual(len(serializer.data), self.FIXTIRED_WORD_LENGTH)


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
        serializer = UserMistakeSerializer(instance=self.user)
        self.assertEqual(serializer.data['id'], str(self.user.id))

    # testing create
    def test_deserialize_mistake_words_correctly(self):
        data = {
            "mistakes": [self.word.id],
        }
        serializer = UserMistakeSerializer(
            data=data, context={'user_id': self.user.id})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(len(serializer.data['words']), 1)

    def test_create_method_function_is_not_replacement_but_adding(self):
        data = {
            "mistakes": [self.word1.id],
        }
        serializer = UserMistakeSerializer(
            data=data, context={'user_id': self.user.id})
        serializer.is_valid()
        serializer.save()
        data = {
            "mistakes": [self.word2.id],
        }
        serializer = UserMistakeSerializer(
            data=data, context={'user_id': self.user.id})
        serializer.is_valid()
        serializer.save()
        self.assertEqual(len(serializer.data['words']), 2)

    def test_patch_mistake_words_correctly(self):
        self.user.mistake_words.add(self.word1, self.word2)
        data = {
            "mistakes": [self.word1.id],
        }
        serializer = UserMistakeSerializer(self.user,
                                           data=data, partial=True, context={'user_id': self.user.id})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(len(serializer.data['words']), 1)
        self.assertEqual(serializer.data['words'][0]['id'], self.word2.id)
