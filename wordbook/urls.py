from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    return_filtered_words, return_wordbook_page, save_mistaken_words
)


urlpatterns = [
    path('languages', TemplateView.as_view(
        template_name='vocabulary/languages.html')),
    path('mistake', save_mistaken_words),
    path('<str:language>/<str:pos>', return_wordbook_page),
    path('data/<str:language>/<str:pos>', return_filtered_words)
]
