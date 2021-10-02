from django.urls import path
from .views import return_words


"""TODO
    path('languages/',  静的テンプレートで)
    path('<language(path_parametar)>/')
    ex: python/noun/, java/adverb/
    path('<language(path_parameter)>/<pos(path_parameter)>/')
"""
urlpatterns = [
    path('words/', return_words, name='words'),
]