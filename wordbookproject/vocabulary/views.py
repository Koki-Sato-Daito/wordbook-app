from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.generic.base import TemplateView

from vocabulary.models import Vocabulary

def forbid_invalid_params(view):
    def _wrapped_view(request, *args, **kwargs):
        if not kwargs['language'] in ['python']:
            return HttpResponseForbidden()
        if not kwargs['pos_param'] in ['noun', 'verb', 'adjective', 'adverb']:
            return HttpResponseForbidden()
        return view(request, *args, **kwargs)
    return _wrapped_view

def return_words(request):
    words = Vocabulary.objects.all()
    context = {'words': words}
    return render(request, 'vocabulary/words.html', context)

@forbid_invalid_params
def return_filtered_words(request, language, pos_param):
    if language == 'python':
        words = Vocabulary.objects.filter(pos=pos_param, python_freq__gt=0)
        data = list(words.values())
        return JsonResponse({'data': data})

@forbid_invalid_params
def return_wordbook_page(request, language, pos_param):
    context = {'language': language, 'pos_param': pos_param}
    return render(request, 'vocabulary/wordbook.html', context)
