from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from progress.models import Progress
from apiv1.serializers.progress_serializers import ProgressSerializer
from apiv1.authorization import get_user_by_authtoken


class ProgressViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """ユーザが試験を中断した際に進捗データをサーバに保存、削除するビューセットクラスです。
    進捗データの取り出しはExamPageAPIViewが担います。
    """
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """ユーザの試験の進捗データをサーバに保存するエンドポイントです。\n
        必ずauthrizationヘッダに認証トークンを入れてリクエストしてください。
        """
        user = get_user_by_authtoken(request)
        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request,  pk, *args, **kwargs):
        """ユーザの試験の進捗データを削除するエンドポイントです。\n
        新たに試験の進捗データを保存したい場合は一度削除してからPOSTリクエストを送ってください。\n
        必ずauthrizationヘッダに認証トークンを入れてリクエストしてください。
        """
        instance = Progress.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
