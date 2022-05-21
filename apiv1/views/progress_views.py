from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from progress.models import Progress
from apiv1.serializers.progress_serializers import ProgressSerializer
from apiv1.permissions import OwnerPermission


"""TODO
Progressビューセットのドキュメント生成処理を追加
"""
class ProgressViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated, OwnerPermission]

    def create(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=request.data['user'])
        self.check_object_permissions(request, user)
        return super().create(request, *args, **kwargs)

    def destroy(self, request,  pk, *args, **kwargs):
        instance = Progress.objects.get(pk=pk)
        user = instance.user
        self.check_object_permissions(request, user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
