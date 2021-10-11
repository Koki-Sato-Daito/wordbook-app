from django.db import models
from accounts.models import User

class Vocabulary(models.Model):
    wordname = models.CharField('単語', max_length=128, unique=True, null=False)
    meaning = models.CharField('意味', max_length=128, null=False)
    pos = models.CharField('品詞', max_length=128, null=False)
    python_freq = models.IntegerField('出現回数(python)', null=False, blank=True)
    mistake_users = models.ManyToManyField(User, related_name='mistake_words')

    class Meta:
        db_table = 'vocabulary'

    def __str__(self):
        return self.wordname
