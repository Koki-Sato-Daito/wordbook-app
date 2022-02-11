from django.urls import path, include
from . import views

app_name = 'apiv1'
urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<uuid:user_id>/mistake/', views.MistakeWordAPIView.as_view()),
    path('words/', views.WordListAPIView.as_view()),
]
