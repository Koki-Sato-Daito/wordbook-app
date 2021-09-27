from vocabulary.models import Vocabulary
from django.shortcuts import render


def return_words(request):
    words = Vocabulary.objects.all()
    context = {'words': words}
    return render(request, 'vocabulary/words.html', context)