from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from progress.models import Progress
from apiv1.serializers.progress_serializers import ProgressSerializer
from apiv1.permissions import OwnerPermission


class ProgressViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """ユーザが試験を中断した際に進捗データをサーバに保存、削除するビューセットクラスです。
    進捗データの取り出しはExamPageAPIViewが担います。
    """
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

    """OwnerPermissionでリクエストしたユーザと、リクエストボディのユーザが同値かをチェックする。
    ProgressSerializerに(リクエストボディに)ユーザのパラメータが必要な理由は、
    Progressモデルの複合ユニーク制約による例外ではなく、ProgressSerializerのvalidateメソッドの例外として
    クライアント側にメッセージを送ったほうがわかりやすいためである。
    このとき、ログイン済みユーザが他のユーザとして進捗データをリクエストできないようにする。"""
    permission_classes = [IsAuthenticated, OwnerPermission]

    def create(self, request, *args, **kwargs):
        """ユーザの試験の進捗データをサーバに保存するエンドポイントです。
        """
        user = get_user_model().objects.get(id=request.data['user'])
        self.check_object_permissions(request, user)
        return super().create(request, *args, **kwargs)

    def destroy(self, request,  pk, *args, **kwargs):
        """ユーザの試験の進捗データを削除するエンドポイントです。
        新たに試験の進捗データを保存したい場合は一度削除してからPOSTリクエストを送ってください。
        """
        instance = Progress.objects.get(pk=pk)
        user = instance.user
        self.check_object_permissions(request, user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
