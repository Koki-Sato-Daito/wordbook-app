from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login_id, password, **extra_fields):
        if not login_id:
            raise ValueError('login_idが入力されていません')
        GlobalUserModel = apps.get_model(self.model._meta.app_label,
                                         self.model._meta.object_name)
        login_id = GlobalUserModel.normalize_username(login_id)
        user = self.model(login_id=login_id, **extra_fields)
        user.password = make_password(password)

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, login_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_admin', False)
        return self._create_user(login_id, password, **extra_fields)
    
    def create_superuser(self, login_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuserはis_staffをTrueにする必要があります')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('superuserはis_adminをTrueにする必要があります')
        
        return self._create_user(login_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ascii_validator = ASCIIUsernameValidator()
    login_id = models.CharField(
        _('login_id'),
        max_length=20,
        unique=True,
        null=False,
        validators=[ascii_validator],
        error_messages={
            'unique': 'login_idがすでに使用されています',
        }
    )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=True)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'
    
    def clean(self):
        super().clean()

    @property
    def is_superuser(self):
        return self.is_admin
