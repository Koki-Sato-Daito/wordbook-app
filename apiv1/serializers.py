from tokenize import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.serializers import TokenSerializer
from rest_framework import serializers

from accounts.models import User
from wordbook.models import Word


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
