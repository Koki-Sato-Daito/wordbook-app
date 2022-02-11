from dataclasses import fields
from rest_framework import serializers
from accounts.models import User
from wordbook.models import Word


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
        source = 'mistake_words',
        many=True,
        write_only=True
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
