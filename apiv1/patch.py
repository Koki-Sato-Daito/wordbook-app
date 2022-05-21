import djoser


class CustomTokenSerializer(djoser.serializers.TokenSerializer):
    user = djoser.serializers.UserSerializer()
    class Meta:
        model = djoser.conf.settings.TOKEN_MODEL
        fields = ("auth_token", "user")


# パッチを適用するメソッドを定義
def patch_djoser_endpoints():
    djoser.serializers.TokenSerializer = CustomTokenSerializer
