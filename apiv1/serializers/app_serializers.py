from rest_framework import serializers

from apiv1.serializers.words_serializers import WordSerializer
from apiv1.serializers.progress_serializers import ProgressSerializer


class InitWordbookPageSerializer(serializers.Serializer):
    words = WordSerializer(many=True)
    progress = ProgressSerializer()
