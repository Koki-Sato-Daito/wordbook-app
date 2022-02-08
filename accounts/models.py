from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('ユーザ名が入力されていません')
        if not email:
            raise ValueError('メールアドレスが入力されていません')
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuserはis_staffをTrueにする必要があります')

        return self._create_user(username, email,  password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='ユーザ名',
        max_length=20,
        help_text='20文字以内で入力してください。文字、数字、いくつかの記号(@ . + - _)が使えます。',
        validators=[username_validator],
        error_messages={
            'unique': '入力されたusernameがすでに使用されています',
        }
    )
    email = models.EmailField(verbose_name='メールアドレス', blank=True, unique=True)

    is_staff = models.BooleanField(_('staff status'), default=True)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @ property
    def is_superuser(self):
        return self.is_staff
