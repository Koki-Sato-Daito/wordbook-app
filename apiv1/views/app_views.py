import uuid
from django.contrib.auth import get_user_model

from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wordbook.models import Word
from progress.models import Progress
from apiv1.serializers.words_serializers import WordSerializer
from apiv1.serializers.app_serializers import InitWordbookPageSerializer
from apiv1.views.words_view import WordFilter


class InitWordbookPageAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        filter = WordFilter(request.query_params)
        if not filter.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # クエリパラメータから値を取得
        language = filter.data.get('language')
        pos = filter.data.get('pos')
        user = None
        if filter.data.get('user'):
            user = get_user_model().objects.get(id=uuid.UUID(filter.data.get('user')))
        mistake = True if request.query_params.get(
            'mistake') == 'true' else False

        words = Word.objects.all()
        if language:
            words = words.filter(language=language)
        if pos:
            words = words.filter(pos=pos)
        if mistake:
            words = words.filter(users=user)
        serializer = WordSerializer(instance=words, many=True)

        progress = None
        if language and pos and user:
            try:
                progress = Progress.objects.get(
                    user=user, language=language, pos=pos, mistake=mistake)
            except Progress.DoesNotExist:
                progress = None
        instance = {'words': words, 'progress': progress}
        serializer = InitWordbookPageSerializer(instance=instance)

        return Response(serializer.data)
