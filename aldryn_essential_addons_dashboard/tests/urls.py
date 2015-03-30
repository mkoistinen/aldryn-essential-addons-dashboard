# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from cms.utils.conf import get_cms_setting

admin.autodiscover()

urlpatterns = patterns('',
    url(
        r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True
        }
    ),
    url(
        r'^media/cms/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': get_cms_setting('MEDIA_ROOT'), 'show_indexes': True
        }
    ),
    url(
        r'^jsi18n/(?P<packages>\S+?)/$',
        'django.views.i18n.javascript_catalog'
    ),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^addons/', include('aldryn_essential_addons_dashboard.urls', namespace='aldryn_essential_addons_dashboard')),
    url(r'^', include('cms.urls')),
)
