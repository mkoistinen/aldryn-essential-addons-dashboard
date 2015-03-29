# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .models import Addon

import warnings


class CsrfExemptMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CsrfExemptMixin, cls).as_view(**initkwargs)
        return csrf_exempt(view)


class ProcessWebhookView(CsrfExemptMixin, View):
    http_method_names = ['post', 'get']

    def get_data(self, request):
        payload = request.POST.get('payload', None)

        warnings.warn('#### Travis data follows...')
        warnings.warn(payload)
        warnings.warn('#### End Travis data. ####')

        return json.loads(payload) if payload else []

    def process_data(self, addon, data):
        # Do yo thang here.
        pass

    def post(self, request, *args, **kwargs):
        # TODO: See: http://docs.travis-ci.com/user/notifications/#Authorization-for-Webhooks
        # Too bad the docs provide the wrong headers!
        slug = request.META.get('HTTP_TRAVIS_REPO_SLUG', None)
        auth = request.META.get('HTTP_AUTHORIZATION', None),
        addon = None
        try:
            addon = Addon.objects.get(repo_slug=slug)
        except Addon.DoesNotExist:
            warnings.warn("Addon '{0}' isn't registered.".format(slug))
            warnings.warn("Here's the request headers:")
            for header, value in request.META.iteritems():
                warnings.warn("{0}: {1}".format(header, value))

        if addon:
            data = self.get_data(request)
            if data:
                self.process_data(addon, data)
        return HttpResponse(status=200)

    def get(self, request, *args, **kwargs):
        """Just for easier testing."""
        print('Received a GET request!')
        return HttpResponse(status=200)
