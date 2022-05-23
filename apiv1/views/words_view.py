from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apiv1.serializers.words_serializers import UserMistakeSerializer
from apiv1.permissions import OwnerPermission


""""TODO
MistakeWordAPIViewのエンドポイントを再考
APIドキュメントの生成
"""


class MistakeWordAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, OwnerPermission]
    serializer_class = UserMistakeSerializer

    def post(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserMistakeSerializer(
            data=request.data, context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def patch(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserMistakeSerializer(user,
                                           data=request.data, partial=True, context={'user_id': user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=user_id)
        self.check_object_permissions(request, user)
        user.mistake_words.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
