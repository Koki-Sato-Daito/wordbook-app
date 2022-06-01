from django.contrib.auth import get_user_model
from rest_framework import serializers

from wordbook.models import Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'wordname', 'meaning', 'pos',
                  'language', 'freq']


User = get_user_model()

class MistakeWordsSerializer(serializers.ModelSerializer):
    """
    ユーザが試験で間違えた単語について以下の責務を持ちます。\n
    Userモデルマネージャの間違えた単語のデータを追加する処理を隠ぺいさせて、serializerから簡単にデータを追加できる。\n
    OpenAPIスキーマのリクエスト、レスポンスの自動生成。\n

    シリアライズには対応していません。単語データはExamPageSerializerでシリアライズを行います。
    """
    class Meta:
        model = User
        fields = ('mistake_words',)
        write_only_fields = ('mistake_words',)

    def create(self, validated_data):
        user = validated_data.get('user')
        words = validated_data.get('mistake_words')
        user.mistake_words.add(*words)
        return user
    

class CorrectWordsSerializer(serializers.ModelSerializer):
    """ユーザが試験で間違えた単語について以下の責務を持ちます。\n
    間違えた単語について再試験の際に正解した場合、ユーザの間違えた単語リストから削除するインターフェースとしてモデルを隠ぺいする\n
    OpenAPIスキーマのリクエスト、レスポンスの自動生成。\n

    シリアライズには対応していません。単語データはExamPageSerializerでシリアライズを行います。
    """
    class Meta:
        model = User
        fields = ('correct_words',)

    correct_words = serializers.PrimaryKeyRelatedField(
        queryset=Word.objects.all(),
        source='mistake_words',
        many=True,
        write_only=True,
    )

    def create(self, validated_data):
        user = validated_data.get('user')
        # sourceの値がキーになることに注意
        words = validated_data.get('mistake_words')
        user.mistake_words.remove(*words)
        return user
    # TODO correct_wordsについてvalidationを書く