import datetime
import random
import string

from djoser import utils
from djoser.conf import settings
from django.contrib.auth import get_user_model
from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apiv1.serializers.accounts_serializers import TokenSerializer


class TokenCreateView(TokenCreateView):
    def _action(self, serializer):
        try:
            settings.TOKEN_MODEL.objects.get(user=serializer.user.id)
            raise PermissionDenied(
                detail={"errors": ["このユーザは他の端末でログインされています。ログアウトしてからお試しください。"]})
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


class GuestLoginAPIView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(10)])
        email_text = random_str + '-' + now + '@example.com'
        user = get_user_model().objects.create_user(
            email=email_text, username="ゲスト", password="pass123")

        token = utils.login_user(request, user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        serializer = TokenSerializer(
            token,
            context={'user': user_data}
        )
        return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
        )
