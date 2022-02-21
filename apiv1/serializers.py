from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.serializers import TokenSerializer
from rest_framework import serializers

from accounts.models import User
from wordbook.models import Word
from progress.models import Progress


class TokenSerializer(TokenSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = self.context['user']
        return response


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'wordname', 'meaning', 'pos',
                  'language', 'freq', 'users']


class UserMistakeSerializer(serializers.ModelSerializer):

    class WordSerializer(serializers.ModelSerializer):
        """
        mistake_words用のシリアライザ
        """
        class Meta:
            model = Word
            fields = ('id', 'wordname', 'meaning', 'pos',
                      'language', 'freq')

    mistakes = serializers.PrimaryKeyRelatedField(
        queryset=Word.objects.all(),
        source='mistake_words',
        many=True,
        write_only=True,

    )

    words = WordSerializer(
        many=True,
        source="mistake_words",
        read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'mistakes', 'words')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        user = get_object_or_404(get_user_model(), id=user_id)
        # user = get_user_model().objects.get(id=user_id)
        words = validated_data.get('mistake_words')
        user.mistake_words.add(*words)
        return user


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['user', 'language', 'pos', 'mistake', 'index']

    def validate(self, validated_data):
        # 複合ユニーク制約のバリデーション
        user = validated_data.get('user')
        language = validated_data.get('language')
        pos = validated_data.get('pos')
        mistake = validated_data.get('mistake')

        already_exist = Progress.objects.filter(
            user=user, language=language, pos=pos, mistake=mistake)
        if already_exist:
            raise serializers.ValidationError(
                'すでに進捗データが存在します。書き換えるには削除してください。'
                f'Progress(user={user}, language={language}, pos={pos}, mistake={mistake}'
            )
        return validated_data 


class InitWordbookPageSerializer(serializers.Serializer):
    words = WordSerializer(many=True)
    progress = ProgressSerializer()
