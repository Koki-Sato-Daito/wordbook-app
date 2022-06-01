from django.contrib.auth import get_user_model
import djoser
from djoser import utils
from drf_spectacular.utils import extend_schema
from rest_framework import status, views
from rest_framework.response import Response

from ..authorization import UserData
from ..patch import CustomTokenSerializer


class GuestLoginAPIView(views.APIView):
    @extend_schema(
        description="ゲストログイン用のエンドポイントです。ゲストアカウントを生成してユーザデータを返します。\n\n\
            Responseのauth_tokenキーについて、実際のキーはキャメルケースのauthTokenであることに注意してください。",
        responses={201: CustomTokenSerializer}
    )
    def post(self, request):
        User = get_user_model()
        user = User.create_guest_account()

        token = utils.login_user(request, user)
        data = UserData(token, user)
        serializer = djoser.serializers.TokenSerializer(data)
        return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
        )
