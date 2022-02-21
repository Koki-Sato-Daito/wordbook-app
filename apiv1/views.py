from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from djoser import utils
from djoser.views import TokenCreateView
from rest_framework import generics, status, mixins, viewsets
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
    users = filters.UUIDFilter(field_name='users')

    class Meta:
        model = Word
        fields = ['pos', 'language', 'users']


class WordListAPIView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = serializers.WordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = WordFilter


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
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Progress.objects.all()
    serializer_class = serializers.ProgressSerializer
    permission_classes = [IsAuthenticated]
