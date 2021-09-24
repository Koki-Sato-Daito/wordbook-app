from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden

from accounts.forms import UserCreationForm
from django.views.generic.edit import CreateView


def logout_required(view):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden()
        return view(request, *args, **kwargs)
    return _wrapped_view


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS,
                             'ユーザー登録に成功しました')
        return HttpResponseRedirect('/')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             'ユーザー登録に失敗しました')
        return super().form_invalid(form)
