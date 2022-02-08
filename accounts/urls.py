from accounts.forms import AuthenticationForm
from .views import SignUpView, logout_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import path

login_view = LoginView.as_view(
    template_name='accounts/login.html',
    redirect_authenticated_user=True,
    form_class=AuthenticationForm
)

urlpatterns = [
    path('signup/', logout_required(SignUpView.as_view()), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
