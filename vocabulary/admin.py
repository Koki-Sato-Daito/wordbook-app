from django.contrib import admin

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from vocabulary.models import Vocabulary

class VocabularyResource(resources.ModelResource):
    mistake_users = fields.Field(
         widget=widgets.IntegerWidget()
    )
    class Meta:
        model = Vocabulary


class VocabularyAdmin(ImportExportModelAdmin):
    filedsets = [
        (None, {'fields': ['wordname', 'meaning', 'pos']}),
        ('Language', {'fields': ['python_freq']},)
    ]

    list_display = ('wordname', 'pos', 'language')
    search_fields = ['wordname', 'meaning']

    resource_class = VocabularyResource


admin.site.register(Vocabulary, VocabularyAdmin)