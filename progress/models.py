import uuid

from django.contrib.auth import get_user_model
from django.db import models

from .validations import validate_language, validate_pos


class Progress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=False)
    language = models.CharField('言語', max_length=20, null=False,
                                validators=[validate_language])
    pos = models.CharField('品詞', max_length=20, null=False,
                           validators=[validate_pos])
    mistake = models.BooleanField('不正解', null=False)
    index = models.IntegerField('インデックス', null=False)
    correctAnswerCounter = models.IntegerField('正解数', null=False)

    class Meta:
        db_table = 'progress'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'language', 'pos', 'mistake'],
                name='progress_unique'
            )
        ]

    def __str__(self):
        return f'Progress({self.user}/{self.language}/{self.pos}/mistake={self.mistake})=index'