from djoser.views import TokenCreateView
from djoser import utils
from rest_framework.response import Response
from rest_framework import status

from apiv1.serializers.accounts_serializers import TokenSerializer


class TokenCreateView(TokenCreateView):
    def _action(self, serializer):
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
