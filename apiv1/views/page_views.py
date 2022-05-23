import uuid

from django.contrib.auth import get_user_model
from accounts.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wordbook.models import Word
from progress.models import Progress
from apiv1.serializers.page_serializers import ExamPageSerializer, ExamPageData


User = get_user_model()

# TODO 
# ドキュメント生成処理の追加
class ExamPageAPIView(generics.GenericAPIView):
    """
    試験画面で必要な単語データと、
    過去にテストを中断した場合の進捗データを
    取得するビュークラスです。
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ExamPageSerializer

    def get(self, request):
        queryset_dict = self.get_queryset_dict()
        filtered_queryset_dict = self.filter_queryset_dict(**queryset_dict)
        instance = ExamPageData(**filtered_queryset_dict)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset_dict(self):
        """Word, Progressの複数リソースをシリアライズするための
        querysetの辞書を返す
        """
        word_queryset = Word.objects.all()
        progress_queryset  = Progress.objects.all()
        return {'words': word_queryset, 'progress': progress_queryset}

    def filter_queryset_dict(self, words=None, progress=None):
        """Word, Progressの複数リソースをシリアライズするためのデータを
        クエリパラメータでフィルタリングしてquerysetの辞書で返す。
        """
        params = self.ParamsCollector(self.request)

        words = words.filter(
            language=params.language).filter(pos=params.pos).order_by('-freq')
        if params.mistake:
            words = words.filter(users=params.user)

        # クエリーパラメータからユーザオブジェクトを取得したときのみProgressデータの取得を試みる
        if params.user:
            try:
                progress = Progress.objects.get(
                    user=params.user, language=params.language, pos=params.pos, mistake=params.mistake)
            except Progress.DoesNotExist:
                progress = None
        else:
            progress = None
        return {'words': words, 'progress': progress}


    class ParamsCollector:
        """ExamPageViewのgetメソッドのクエリーパラメータ
        から必要なデータに変換して保持します。
        言語、品詞については文字列型、ユーザはモデル、
        ユーザが過去に間違った問題はmistakeにブール値で表現されます。
        """
        language: str
        pos: str
        user = None
        mistake: bool

        def __init__(self, request) -> None:
            self.language = request.query_params.get('language')
            self.pos = request.query_params.get('pos')
            if user_pk_str := request.query_params.get('user'):
                self.user = User.get_user_by_pk_str(user_pk_str)
            self.mistake = True if request.query_params.get('mistake') == "true" else False



