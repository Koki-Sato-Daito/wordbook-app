from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wordbook.models import Word
from .serializers import WordSerializer, UserMistakeSerializer


class WordFilter(filters.FilterSet):
    language = filters.CharFilter(field_name='language')
    pos = filters.CharFilter(field_name='pos')
    users = filters.UUIDFilter(field_name='users')

    class Meta:
        model = Word
        fields = ['pos', 'language', 'users']


class WordListAPIView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = WordFilter


class MistakeWordAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMistakeSerializer

    def post(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=user_id)
        serializer = UserMistakeSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=user_id)
        user.mistake_words.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
