from django.urls import path
from django.views.generic.base import TemplateView
from .views import return_words


"""TODO
    ex: python/noun/, java/adverb/
    path('<language(path_parameter)>/<pos(path_parameter)>/')
"""
urlpatterns = [
    path('words/', return_words, name='words'),
    path('languages/', TemplateView.as_view(
        template_name='vocabulary/languages.html'), name='languages')
]