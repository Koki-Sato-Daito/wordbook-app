import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.views.decorators.http import require_POST

from wordbook.models import Word

@login_required
@require_POST
def save_mistaken_words(request):
    words = json.loads(request.body).get('words')
    request.user.mistake_words.clear()
    
    for mistake_index in words:
        word = Word.objects.get(pk=mistake_index)
        word.mistake_users.add(request.user)
    return HttpResponse()
