from django.contrib.auth import get_user_model
from djoser.conf import settings
from rest_framework.authtoken.models import Token


# TODO ユニットテストの追加
def get_user_by_authtoken(request):
    """認証トークンからユーザオブジェクトを取得します。
    """
    token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
    return Token.objects.get(key=token).user


class UserData:
    """ログイン時にクライアントに渡すデータクラスです。
    認証キーとユーザデータを格納しログイン系のシリアライザに渡すことができます。
    """
    key: settings.TOKEN_MODEL
    user: get_user_model()

    def __init__(self, auth_token, user):
        self.key = auth_token
        self.user = user

    def __str__(self) -> str:
        return f"UserData(auth_token={self.key}, user={self.user})"

