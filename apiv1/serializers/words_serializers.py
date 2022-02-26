from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers

from wordbook.models import Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'wordname', 'meaning', 'pos',
                  'language', 'freq', 'users']


class UserMistakeSerializer(serializers.ModelSerializer):

    class WordSerializer(serializers.ModelSerializer):
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
        model = get_user_model()
        fields = ('id', 'mistakes', 'words')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        user = get_object_or_404(get_user_model(), id=user_id)
        words = validated_data.get('mistake_words')
        user.mistake_words.add(*words)
        return user
    
    def update(self, instance, validated_data):
        correct_words = validated_data.get('mistake_words')
        for words in correct_words:
            instance.mistake_words.remove(words)
        return instance