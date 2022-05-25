from rest_framework.authtoken.models import Token


# TODO ユニットテストの追加
def get_user_by_authtoken(request):
    """認証トークンからユーザオブジェクトを取得します。
    """
    token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
    return Token.objects.get(key=token).user
