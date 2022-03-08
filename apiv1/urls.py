from django.urls import path, include
from rest_framework import routers
from apiv1.views.accounts_views import TokenCreateView, GuestLoginAPIView
from apiv1.views.app_views import InitWordbookPageAPIView
from apiv1.views.progress_views import ProgressViewSet
from apiv1.views.words_view import MistakeWordAPIView

router  = routers.SimpleRouter()
router.register('', ProgressViewSet)

app_name = 'apiv1'
urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view()),
    path('auth/', include('djoser.urls.base')),
    path('auth/', include('djoser.urls.authtoken')),
    path('guest_login/', GuestLoginAPIView.as_view()),
    
    path('init_wordbook_page/', InitWordbookPageAPIView.as_view()),
    path('users/<uuid:user_id>/mistake/', MistakeWordAPIView.as_view()),
    path('progress/', include(router.urls)),
]
