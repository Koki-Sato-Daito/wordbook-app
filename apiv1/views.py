import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from djoser import utils
from djoser.views import TokenCreateView
from rest_framework import generics, status, mixins, viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wordbook.models import Word
from progress.models import Progress
from apiv1 import serializers


class TokenCreateView(TokenCreateView):
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        user = serializer.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        token_serializer_class = serializers.TokenSerializer(
            token,
            context={'user': user_data}
        )
        return Response(
            data=token_serializer_class.data,
            status=status.HTTP_200_OK
        )


class WordFilter(filters.FilterSet):
    language = filters.CharFilter(field_name='language')
    pos = filters.CharFilter(field_name='pos')
    users = filters.UUIDFilter(field_name='user')

    class Meta:
        model = Word
        fields = ['pos', 'language', 'users']


class MistakeWordAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserMistakeSerializer

    def post(self, request, user_id, *args, **kwargs):
        serializer = serializers.UserMistakeSerializer(
            data=request.data, context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=user_id)
        user.mistake_words.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProgressViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Progress.objects.all()
    serializer_class = serializers.ProgressSerializer
    permission_classes = [IsAuthenticated]


class InitWordbookPageAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        filter = WordFilter(request.query_params)
        if not filter.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        language = filter.data.get('language')
        pos = filter.data.get('pos')
        user = None
        user_id = filter.data.get('user')
        if user_id:
            user = get_user_model().objects.get(id=uuid.UUID(user_id))
        mistake = True  if request.query_params.get('mistake')=="true" else False

        words = Word.objects.all()
        if language:
            words = words.filter(language=language)
        if pos:
            words = words.filter(pos=pos)
        if user and mistake:
            words = words.filter(users=user)
        serializer = serializers.WordSerializer(instance=words, many=True)
        
        progress = None
        if language and pos and user:
            try:
                progress = Progress.objects.all().get(
                    user=user, language=language, pos=pos, mistake=mistake)
            except Progress.DoesNotExist:
                progress = None
        instance = {'words': words, 'progress': progress}
        serializer = serializers.InitWordbookPageSerializer(instance=instance)

        return Response(serializer.data)
