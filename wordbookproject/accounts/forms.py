from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm,
    UsernameField
)
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _ 

from .models import User


UserModel = get_user_model()

class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ("login_id",)


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ("login_id",)


class AuthenticationForm(forms.Form):
    login_id = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label = _('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'}),
    )

    error_messages = {
        'invalid_login': _(
            "正しいログインIDとパスワードを入力してください。"
        ),
        'inactive': _('This account is inactive'),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_chache = None
        super().__init__(*args, **kwargs)

        # loginid フィールドのmax_lengthとlabelを設定します。
        self.loginid_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        loginid_max_length = self.loginid_field.max_length or 32
        self.fields['login_id'].max_length = loginid_max_length
        self.fields['login_id'].widget.attrs['maxlength'] = loginid_max_length
        if self.fields['login_id'].label is None:
            self.fields['login_id'].label = capfirst(self.loginid_field.verbose_name)

    def clean(self):
        super().clean()
        login_id = self.cleaned_data.get('login_id')
        password = self.cleaned_data.get('password')

        if login_id is not None and password:
            self.user_cache = authenticate(self.request, login_id=login_id, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'login_id': self.loginid_field.verbose_name},
        )
