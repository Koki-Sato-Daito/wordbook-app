from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apiv1.serializers.words_serializers import CorrectWordsSerializer, MistakeWordsSerializer
from apiv1.authorization import get_user_by_authtoken


"""TODO
APIドキュメントの生成
クライアント側のAPIコール処理を修正
"""

class MistakeWordsAPIView(mixins.CreateModelMixin,
                                        mixins.DestroyModelMixin,
                                        generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MistakeWordsSerializer

    @extend_schema(
        responses={201: MistakeWordsSerializer}
    )
    def post(self, request, *args, **kwargs):
        """間違えた問題を記録するエンドポイントです。\n
        必ずAuthenticationヘッダに認証トークンをつけてリクエストします。\n
        """
        user = get_user_by_authtoken(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """DBに登録された間違えた問題を一括で削除します。\n
        認証トークンによって識別されたユーザのデータに対して適用されます。\n
        従って必ずAuthenticationヘッダに認証トークンを含めてリクエストします。
        """
        user = get_user_by_authtoken(request)
        user.mistake_words.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CorrectWordsAPIView(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CorrectWordsSerializer

    @extend_schema(
        responses={201: CorrectWordsSerializer}
    )
    def post(self, request, *args, **kwargs):
        """復習ページにて正解した問題を記録するエンドポイントです。間違った問題は復習ページで一度正解するとリストから削除されます。\n
        必ずAuthenticationヘッダに認証トークンをつけてリクエストしてください。\n
        リクエストボディのリストには正解した単語のIDが入ります。
        """
        user = get_user_by_authtoken(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
