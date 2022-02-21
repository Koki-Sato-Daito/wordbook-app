from django.core.exceptions import ValidationError

from wordbook.models import Word


def validate_language(language):
    language_list = Word.objects.values_list('language')
    print(language)
    print(language_list)
    if not language in language_list:
        raise ValidationError(f'{language}という言語には対応していません。')


def validate_pos(pos):
    pos_list = ['noun', 'verb', 'adjective', 'adverb']
    if not pos in pos_list:
        raise ValidationError(f'{pos}という品詞には対応していません。')
