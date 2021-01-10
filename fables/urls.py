"""
This module provides the URL Configuration for **fables**.

The ``urlpatterns`` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/3.0/topics/http/urls/

"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.organizations.urls')),
    path('api/', include('apps.payments.urls'))
]

admin.site.site_header = 'Fables Administration'
admin.site.index_title = 'Site Administration'
admin.site.site_title = 'Fables Administration'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
