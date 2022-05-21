from django.contrib.auth import get_user_model
import djoser
from djoser import utils
from drf_spectacular.utils import extend_schema
from rest_framework import status, views
from rest_framework.response import Response

from accounts.user_data import UserData
from ..patch import CustomTokenSerializer


"""TODO
responseのauh_tokenがスネークケースなので修正
"""
class GuestLoginAPIView(views.APIView):
    @extend_schema(
        description="ゲストログイン用のエンドポイントです。ゲストアカウントを生成してユーザデータを返します。",
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
