from django.urls import path, include, re_path
from rest_framework import routers
import djoser
import djoser.urls.base as djoser_base
import djoser.urls.authtoken as djoser_token

from apiv1.views.accounts_views import GuestLoginAPIView
from apiv1.views.page_views import ExamPageAPIView
from apiv1.views.progress_views import ProgressViewSet
from apiv1.views.words_view import CorrectWordsAPIView, MistakeWordsAPIView
from apiv1.views.not_found_views import NotFoundAPIView

from .patch import patch_djoser_endpoints


patch_djoser_endpoints()

djoser_token.urlpatterns = [
    re_path(r"^token/login/?$", djoser.views.TokenCreateView.as_view()),
    re_path(r"^token/logout/?$", djoser.views.TokenDestroyView.as_view()),
    path('guest_login/', GuestLoginAPIView.as_view()),
]

progress_router  = routers.SimpleRouter()
progress_router.register('', ProgressViewSet)

app_name = 'apiv1'
urlpatterns = [
    path('', include('djoser.urls.base')),
    path('auth/', include('djoser.urls.authtoken')),

    path('exam_page_data/', ExamPageAPIView.as_view()),
    path('progress/', include(progress_router.urls)),
    path('mistake_words/',  MistakeWordsAPIView.as_view()),
    path('correct_words/',  CorrectWordsAPIView.as_view()),

    re_path(r'', NotFoundAPIView.as_view()) 
]
