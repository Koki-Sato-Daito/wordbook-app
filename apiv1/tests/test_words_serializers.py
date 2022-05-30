from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apiv1.serializers.words_serializers import WordSerializer, MistakeWordsSerializer, CorrectWordsSerializer
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


class TestMistakeWordsSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    user = None
    word = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')
        cls.word = cls.word1 = Word.objects.get(pk=1)
        cls.word2 = Word.objects.get(pk=2)

    def test_deserialize_mistake_words_correctly(self):
        """デシリアライズとcreateメソッドのテスト
        """
        data = {
            "mistake_words": [self.word.id],
        }
        serializer = MistakeWordsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.user)
        self.assertEqual(serializer.data['mistake_words'][0], 1)

    # testing create
    def test_create_method_is_not_replacement_but_adding(self):
        """createメソッドは新しいレコードは追加するが、既存のレコードは削除しないことをテスト
        """
        data = {
            "mistake_words": [self.word1.id],
        }
        serializer = MistakeWordsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.user)
        data = {
            "mistake_words": [self.word2.id],
        }
        serializer = MistakeWordsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.user)
        self.assertEqual(len(self.user.mistake_words.all()), 2)

    def test_create_method_can_add_plural_words(self):
        """複数の単語を追加するテスト
        """
        data = {
            "mistake_words": [self.word1.id, self.word2.id]
        }
        serializer = MistakeWordsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.user)
        self.assertEqual(len(self.user.mistake_words.all()), 2)


class TestCorrectWordsSerializer(APITestCase):
    fixtures = ['users.json', 'words.json']
    user = None
    word = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.get(username='test1')
        cls.word = cls.word1 = Word.objects.get(pk=1)
        cls.word2 = Word.objects.get(pk=2)

    def test_create_method_can_remove_mistake_words(self):
        """createメソッドのテスト
        """
        self.user.mistake_words.add(self.word1, self.word2)
        data = {
            "correct_words": [self.word1.id],
        }
        serializer = CorrectWordsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.user)
        self.assertEqual(len(self.user.mistake_words.all()), 1)
        self.assertEqual(self.user.mistake_words.all()[0].id, 2)

    def test_create_method_can_remove_plural_mitake_words(self):
        """複数の単語を削除するテスト
        """
        self.user.mistake_words.add(self.word1, self.word2)
        data = {
            "correct_words": [self.word1.id, self.word2.id],
        }
        serializer = CorrectWordsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.user)
        self.assertEqual(len(self.user.mistake_words.all()), 0)
