from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apiv1.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('api-auth/', include('rest_framework.urls')),
        path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), 
        path('docs/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), 
    ]
