import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
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
        words = Vocabulary.objects.filter(pos=pos_param, python_freq__gt=0).order_by("-python_freq")

    if request.GET.get('mistake') == "True":
        words = words.filter(mistake_users=request.user)

    data = list(words.values())
    return JsonResponse({'data': data})

@forbid_invalid_params
def return_wordbook_page(request, language, pos_param):
    context = {
        'language': language,
        'pos_param': pos_param,
        'mistake': request.GET.get('mistake')
    }
    return render(request, 'vocabulary/wordbook.html', context)

@login_required
@require_POST
def save_mistaken_words(request):
    words = json.loads(request.body).get('words')
    request.user.mistake_words.clear()
    
    for mistake_index in words:
        word = Vocabulary.objects.get(pk=mistake_index)
        word.mistake_users.add(request.user)
    return HttpResponse()
