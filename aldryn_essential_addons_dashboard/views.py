# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import re

from django.db.models import Q
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, View
from django.utils.timezone import now

from versionfield.version import Version
from versionfield.constants import DEFAULT_NUMBER_BITS

from .models import Addon

import warnings

ZERO = Version('0.0.0', DEFAULT_NUMBER_BITS)


class CsrfExemptMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CsrfExemptMixin, cls).as_view(**initkwargs)
        return csrf_exempt(view)


class AddonListView(ListView):
    http_method_names = ['get', ]
    model = Addon


class AddonDetailView(DetailView):
    http_method_names = ['get', ]
    model = Addon


class ProcessTravisWebhookView(CsrfExemptMixin, View):
    http_method_names = ['post', 'get']

    def get_data(self, request):
        payload = request.POST.get('payload', None)
        return json.loads(payload) if payload else []

    def get_job_python(self, job):
        """
        Given a single 'job' object, return the found Python.

        Returns a Version object or None
        """
        if job['config'] and job['config']['python']:
            # json may convert '1.6' into a float, force a string.
            return Version(str(job['config']['python']), DEFAULT_NUMBER_BITS)
        return None

    def get_max_python(self, matrix):
        """Returns the max. version of python in all the successful jobs."""
        max_python = ZERO
        for job in matrix:
            if job["state"] == "finished" and job["status"] == 0:
                job_python = self.get_job_python(job)
                if job_python and job_python > max_python:
                    max_python = job_python
        if max_python > ZERO:
            return max_python
        return None

    def get_job_django(self, job):
        """
        Given a single 'job' object, return the found Django. This one is a bit
        trickier as we'll have to parse it out of the ENV.

        Returns a Version object or None
        """
        pattern = re.compile('.*?django *= *(?P<version>[0-9][0-9.]*).*?', re.I)
        if job['config'] and job['config']['env']:
            match = re.match(pattern, job['config']['env'])
            if match:
                return Version(match.groups('django')[0], DEFAULT_NUMBER_BITS)
        return None

    def get_max_django(self, matrix):
        """Returns the max. version of django in all the successful jobs."""
        max_django = ZERO
        for job in matrix:
            if job['state'] == 'finished' and job['status'] == 0:
                job_django = self.get_job_django(job)
                if job_django and job_django > max_django:
                    max_django = job_django
        if max_django > ZERO:
            return max_django
        return None

    def process_data(self, addon, data):
        if data and data['matrix']:
            addon.last_webhook_timestamp = now()
            addon.max_python_version = self.get_max_python(data['matrix'])
            addon.max_django_version = self.get_max_django(data['matrix'])
            addon.build_passing = data['status'] == 0
            warnings.warn('Updating "{0}" with: {1}, {2}, {3}'.format(
                addon,
                addon.max_python_version,
                addon.max_django_version,
                addon.build_passing,
            ))
        return

    def post(self, request, *args, **kwargs):
        # TODO: See: http://docs.travis-ci.com/user/notifications/#Authorization-for-Webhooks
        # Too bad the docs provide the wrong headers!
        slug = request.META.get('HTTP_TRAVIS_REPO_SLUG', None)
        auth = request.META.get('HTTP_AUTHORIZATION', None),
        addon = None
        try:
            # We'll also match those with an empty auth_digest, and if found,
            # we'll populate it with what Travis supplies. This should only
            # happen the first time the webhook fires and only if we haven't
            # already set the token ourselves.
            addon = Addon.objects.get(
                Q(auth_digest=auth) | Q(auth_degest__isnull=True),
                repo_slug=slug
            )

            # See note above
            if not addon.auth_digest:
                addon.auth_digest = auth    # Save deferred

        except Addon.DoesNotExist:
            pass

        if addon:
            self.process_data(addon, self.get_data(request))
            addon.save()
        return HttpResponse(status=200)

    def get(self, request, *args, **kwargs):
        """Just for easier testing."""
        return TemplateResponse(request,
            'aldryn_essential_addons_dashboard/url_ok.html', {})
