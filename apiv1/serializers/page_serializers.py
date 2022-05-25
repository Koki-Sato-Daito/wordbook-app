from dataclasses import dataclass
from rest_framework import serializers

from apiv1.serializers.words_serializers import WordSerializer
from apiv1.serializers.progress_serializers import ProgressSerializer


class ExamPageSerializer(serializers.Serializer):
    """試験ページのマスタデータをシリアライズするクラスです。
    デシリアライズ(リクエスト時などの辞書->クエリーセットオブジェクトへの変換)には対応していません。

    Word, Progressのどちらかをデシリアライズをするケースは各々のエンドポイントで行います。
    """
    words = WordSerializer(many=True)
    progress = ProgressSerializer()


class ExamPageData:
    """WordのクエリーセットとProgressのクエリーセットをシリアライズするときに
    シリアライザに渡すオブジェクトを生成します。
    """
    words = None
    progress = None

    def __init__(self, words, progress) -> None:
        self.words = words
        self.progress = progress
