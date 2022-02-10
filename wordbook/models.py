from django.db import models


class Word(models.Model):
    wordname = models.CharField('単語', max_length=128, null=False)
    meaning = models.CharField('意味', max_length=128, null=False)
    pos = models.CharField('品詞', max_length=128, null=False)
    language = models.CharField('言語', max_length=128, null=False)
    freq = models.IntegerField('出現回数', null=False, blank=True)

    class Meta:
        db_table = 'words'

    def __str__(self):
        return f'{self.wordname}[{self.pos}]'
