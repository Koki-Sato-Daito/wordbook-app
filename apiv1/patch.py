import djoser
from drf_spectacular.utils import extend_schema


class CustomTokenSerializer(djoser.serializers.TokenSerializer):
    user = djoser.serializers.UserSerializer()
    class Meta:
        model = djoser.conf.settings.TOKEN_MODEL
        fields = ("auth_token", "user")

"""TODO
responseのauh_tokenがスネークケースなので修正
"""
@extend_schema(
    description="ログイン用のエンドポイントです。\
        デフォルトのdjoserのログインエンドポイントとレスポンスが変わっているため注意してください。",
    responses={201: CustomTokenSerializer}
)
class CustomTokenCreateView(djoser.views.TokenCreateView):
    pass


# パッチを適用するメソッドを定義
def patch_djoser_endpoints():
    djoser.serializers.TokenSerializer = CustomTokenSerializer
    djoser.views.TokenCreateView = CustomTokenCreateView
