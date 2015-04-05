# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import AddonDetailView, AddonListView, TravisWebhookView, GitHubWebhookView


urlpatterns = patterns('',

    # This is the Travis Webhook endpoint..
    url(
        r'^travis-endpoint/$',
        TravisWebhookView.as_view(),
        name='process-travis-webhook',
    ),

    url(
        r'^github-endpoint/$',
        GitHubWebhookView.as_view(),
        name='process-travis-webhook',
    ),

    url(
        r'^(?P<slug>[-\w]+)/$',
        AddonDetailView.as_view(),
        name='addon-detail'
    ),

    url(
        r'^$',
        AddonListView.as_view(),
        name='addon-list'
    ),
)
