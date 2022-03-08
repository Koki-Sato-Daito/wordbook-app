from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apiv1.serializers.accounts_serializers import TokenSerializer


class TokenCreateView(TokenCreateView):
    def _action(self, serializer):
        try:
            settings.TOKEN_MODEL.objects.get(user=serializer.user.id)
            raise PermissionDenied(detail={"errors": ["このユーザは他の端末でログインされています。ログアウトしてからお試しください。"]})
        except settings.TOKEN_MODEL.DoesNotExist:
            token = utils.login_user(self.request, serializer.user)
            user = serializer.user
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            token_serializer_class = TokenSerializer(
                token,
                context={'user': user_data}
            )
            return Response(
                data=token_serializer_class.data,
                status=status.HTTP_200_OK
            )
