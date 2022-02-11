from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apiv1.serializers import WordSerializer, UserMistakeSerializer
from wordbook.models import Word


class TestWordSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    FIXTIRED_WORD_LENGTH = 6

    # testing deserialize
    def test_deserialize_simple_word(self):
        serializer = WordSerializer(instance=Word.objects.get(pk=1))
        self.assertEqual(serializer.data['wordname'], 'apple')

    def test_deserialize_list_words(self):
        serializer = WordSerializer(instance=Word.objects.all(), many=True)
        self.assertEqual(len(serializer.data), self.FIXTIRED_WORD_LENGTH)

    def test_deserialize_users_data(self):
        for i in range(1, 3):
            get_user_model().objects.get(
                username=f'test{i}').mistake_words.add(1)
        serializer = WordSerializer(instance=Word.objects.get(pk=1))
        self.assertEqual(len(serializer.data['users']), 2)


class TestUserMistakeSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    user = None
    word = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')
        cls.word = Word.objects.get(pk=1)

    # testing deserialize
    def test_deserialize_users_mistake_words_correctly(self):
        serializer = UserMistakeSerializer(instance=self.user)
        self.assertEqual(serializer.data['id'], str(self.user.id))

    # testing serialize
    def test_serialize_mistake_words_correctly(self):
        data = {
            "mistakes": [self.word.id],
        }
        serializer = UserMistakeSerializer(
            instance=self.user, data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        print(self.user.mistake_words)
        self.assertEqual(len(serializer.data['words']), 1)
