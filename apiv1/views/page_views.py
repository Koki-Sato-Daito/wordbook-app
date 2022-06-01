from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wordbook.models import Word
from progress.models import Progress
from apiv1.authorization import get_user_by_authtoken
from apiv1.serializers.page_serializers import ExamPageSerializer, ExamPageData


User = get_user_model()


class ExamPageAPIView(generics.GenericAPIView):
    """
    試験画面で必要な単語データと、
    過去にテストを中断した場合の進捗データを
    取得するビュークラスです。
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ExamPageSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter('language', OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter('pos', OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter('mistake', OpenApiTypes.BOOL, OpenApiParameter.QUERY),
        ]
    )
    def get(self, request):
        """試験画面で必要な単語リストと、
        試験の進捗状態を返すエンドポイントです。\n
        単語リストは各種クエリーパラメータでフィルタリングして返します。\n
        また、もしユーザが試験を中断していた場合は途中経過の進捗データを返します。\n
        レスポンスの'progress'の中にはidが含まれます。
        Progressデータを削除する時に使うためクライアントで保持するように実装してください。
        """
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
        パラメータでフィルタリングしてquerysetの辞書で返す。
        """
        params = self.ParamsCollector(self.request)
        words = words.filter(
            language=params.language).filter(pos=params.pos).order_by('-freq')
        if params.mistake:
            words = words.filter(users=params.user)

        try:
            progress = Progress.objects.get(
                user=params.user, language=params.language, pos=params.pos, mistake=params.mistake)
        except Progress.DoesNotExist:
            progress = None
        return {'words': words, 'progress': progress}


    class ParamsCollector:
        """ExamPageViewのgetメソッドのクエリーパラメータとヘッダーから必要なデータに変換して保持します。
        言語、品詞については文字列型、ユーザはモデル、
        ユーザが過去に間違った問題でフィルタリングするかはmistakeにブール値で表現されます。
        """
        language: str
        pos: str
        user = None
        mistake: bool

        def __init__(self, request) -> None:
            self.language = request.query_params.get('language')
            self.pos = request.query_params.get('pos')
            self.user = get_user_by_authtoken(request)
            self.mistake = True if request.query_params.get('mistake') == "true" else False
