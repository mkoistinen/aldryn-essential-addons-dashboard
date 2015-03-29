# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class CsrfExemptMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CsrfExemptMixin, cls).as_view(**initkwargs)
        return csrf_exempt(view)


class AuthenticateRequestMixin(object):
    # TODO: See: http://docs.travis-ci.com/user/notifications/#Authorization-for-Webhooks
    pass


class ProcessWebhookView(CsrfExemptMixin, AuthenticateRequestMixin, View):
    http_method_names = ['post', 'get']

    def get_data(self, request):
        payload = request.POST.get('payload', None)
        return json.loads(payload) if payload else []

    def post(self, request, *args, **kwargs):
        data = self.get_data(request)
        # Do yo thang here.
        print(data)
        return HttpResponse(status=200)

    def get(self, request, *args, **kwargs):
        """Just for easier testing."""
        print('Received a GET request!')
        return HttpResponse(status=200)
