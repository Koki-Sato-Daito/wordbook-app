from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from wordbook.models import Word
from .serializers import WordSerializer


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

# http://localhost:8000/api/v1/words/1/users/1 でwords-usersにレコードを作うう