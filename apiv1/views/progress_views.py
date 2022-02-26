from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from progress.models import Progress
from apiv1.serializers.progress_serializers import ProgressSerializer


class ProgressViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]
