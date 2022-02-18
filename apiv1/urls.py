from django.urls import path, include
from . import views

app_name = 'apiv1'
urlpatterns = [
    path('auth/token/login/', views.TokenCreateView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<uuid:user_id>/mistake/', views.MistakeWordAPIView.as_view()),
    path('words/', views.WordListAPIView.as_view()),
]
