from dataclasses import dataclass
from rest_framework import serializers

from apiv1.serializers.words_serializers import WordSerializer
from apiv1.serializers.progress_serializers import ProgressSerializer


class ExamPageSerializer(serializers.Serializer):
    words = WordSerializer(many=True)
    progress = ProgressSerializer()


class ExamPageData:
    words = None
    progress = None

    def __init__(self, words, progress) -> None:
        self.words = words
        self.progress = progress
