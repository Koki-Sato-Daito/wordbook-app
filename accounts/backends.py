from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()

class CustomBackend(ModelBackend):
    def authenticate(self, request, login_id=None, password=None):
        if login_id is None or password is None:
            return None
        try:
            user = UserModel.objects.get(login_id=login_id)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
