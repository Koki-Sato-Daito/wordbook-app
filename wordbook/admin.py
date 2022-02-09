from django.contrib import admin

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from wordbook.models import Word

class WordResource(resources.ModelResource):
    mistake_users = fields.Field(
         widget=widgets.IntegerWidget()
    )
    class Meta:
        model = Word


class WordAdmin(ImportExportModelAdmin):
    filedsets = [
        (None, {'fields': ['wordname', 'meaning', 'pos']}),
        ('Language', {'fields': ['freq']},)
    ]

    list_display = ('wordname', 'pos', 'language')
    search_fields = ['wordname', 'meaning']

    resource_class = WordResource


admin.site.register(Word, WordAdmin)