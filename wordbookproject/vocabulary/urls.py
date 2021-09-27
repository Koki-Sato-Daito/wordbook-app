from django.urls import path
from .views import return_words


urlpatterns = [
    path('words/', return_words, name='words')
]