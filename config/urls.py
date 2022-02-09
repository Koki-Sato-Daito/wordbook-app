from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


from config.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='top.html'), name='top'),
    path('api/v1/', include('apiv1.urls')),
    path('vocabulary/', include('vocabulary.urls')),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
