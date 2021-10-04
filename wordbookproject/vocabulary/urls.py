from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    return_filtered_words, return_wordbook_page
)


urlpatterns = [
    path('languages', TemplateView.as_view(
        template_name='vocabulary/languages.html'), name='languages'),
    path('<str:language>/<str:pos_param>', return_wordbook_page, name='wordbook'),
    path('data/<str:language>/<str:pos_param>', return_filtered_words, name='vocabulary_data')
]