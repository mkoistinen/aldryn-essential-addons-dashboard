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
        return json.loads(payload) if payload else []

    def process_data(addon, data):
        # Do yo thang here.
        warnings.warn('#### Travis data follows...')
        warnings.warn(data)
        warnings.warn('#### End Travis data.')

    def post(self, request, *args, **kwargs):
        # TODO: See: http://docs.travis-ci.com/user/notifications/#Authorization-for-Webhooks
        slug = request.META.get('Travis-Repo-Slug', None)
        auth = request.META.get('Authorization', None),
        try:
            addon = Addon.objects.get(repo_id=slug)
        except Addon.DoesNotExist:
            pass

        if addon:
            data = self.get_data(request)
            if data:
                self.process_data(addon, data)
        return HttpResponse(status=200)

    def get(self, request, *args, **kwargs):
        """Just for easier testing."""
        print('Received a GET request!')
        return HttpResponse(status=200)
