from django.contrib.auth import get_user_model
from djoser.conf import settings

class UserData:
    key: settings.TOKEN_MODEL
    user: get_user_model()

    def __init__(self, auth_token, user):
        self.key = auth_token
        self.user = user

    def __str__(self) -> str:
        return f"UserData(auth_token={self.key}, user={self.user})"

