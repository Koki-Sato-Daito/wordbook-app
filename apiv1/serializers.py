from dataclasses import fields
from rest_framework import serializers
from wordbook.models import Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['wordname', 'meaning', 'pos',
                  'language', 'freq']
