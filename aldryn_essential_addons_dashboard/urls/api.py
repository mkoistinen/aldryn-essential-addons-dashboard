# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from ..views import ProcessWebhookView

urlpatterns = patterns('',
    url(r'^$', ProcessWebhookView.as_view(), name='process-webhook'),
)
