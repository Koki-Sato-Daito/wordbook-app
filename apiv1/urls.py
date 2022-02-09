from django.urls import path, include

app_name = 'apiv1'
urlpatterns = [
    path('auth/', include('djoser.urls.authtoken'))
]
