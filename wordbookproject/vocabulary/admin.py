from django.contrib import admin

from vocabulary.models import Vocabulary


class VocabularyAdmin(admin.ModelAdmin):
    filedsets = [
        (None, {'fields': ['wordname', 'meaning', 'pos']}),
        ('Language', {'fields': ['python_freq']},)
    ]

    list_display = ('wordname', 'pos')
    search_fields = ['wordname', 'meaning']

admin.site.register(Vocabulary, VocabularyAdmin)