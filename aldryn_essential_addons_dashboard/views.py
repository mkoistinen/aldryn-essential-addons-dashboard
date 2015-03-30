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

ZERO = Version('0.0.0', DEFAULT_NUMBER_BITS)
MAX  = Version('255.255.65535', DEFAULT_NUMBER_BITS)


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
        data = json.loads(payload) if payload else []
        return data

    def get_job_python(self, job):
        """
        Given a single 'job' object, return the found Python.

        Returns a Version object or None
        """
        if 'config' in job and 'python' in job['config']:
            # json may convert '1.6' into a float, force a string.
            return Version(str(job['config']['python']), DEFAULT_NUMBER_BITS)
        return None

    def get_python_range(self, matrix):
        """Returns the max. version of python in all the successful jobs."""
        max_python = ZERO
        min_python = MAX
        job_python = None
        for job in matrix:
            if ('state' in job and job['state'] == 'finished' and
                    'status' in job and job['status'] == 0):
                job_python = self.get_job_python(job)
                if job_python:
                    if int(job_python) > int(max_python):
                        max_python = Version(str(job_python), DEFAULT_NUMBER_BITS)
                    if int(job_python) < int(min_python):
                        min_python = Version(str(job_python), DEFAULT_NUMBER_BITS)
        if max_python == ZERO or min_python == MAX:
            return (None, None)
        return (min_python, max_python)

    def get_job_django(self, job):
        """
        Given a single 'job' object, return the found Django. This one is a bit
        trickier as we'll have to parse it out of the ENV.

        Returns a Version object or None
        """
        pattern = re.compile('.*?django *= *(?P<version>[0-9][0-9.]*).*?', re.I)
        if 'config' in job and job['config'] and 'env' in job['config']:
            match = re.match(pattern, job['config']['env'])
            if match:
                return Version(match.groups('django')[0], DEFAULT_NUMBER_BITS)
        return None

    def get_django_range(self, matrix):
        """Returns the max. version of django in all the successful jobs."""
        max_django = ZERO
        min_django = MAX
        for job in matrix:
            if ('state' in job and job['state'] == 'finished'
                    and job['status'] == 0):
                job_django = self.get_job_django(job)
                if job_django:
                    if int(job_django) > int(max_django):
                        max_django = Version(str(job_django), DEFAULT_NUMBER_BITS)
                    if int(job_django) < int(min_django):
                        min_django = Version(str(job_django), DEFAULT_NUMBER_BITS)
        if max_django == ZERO or min_django == MAX:
            return (None, None)
        return (min_django, max_django)

    def process_data(self, addon, data):
        if addon and data and 'matrix' in data:
            right_now = now()
            addon.last_webhook_timestamp = right_now
            # Only modify the python/django versions when build was a success.
            if 'status' in data and data['status'] == 0:
                addon.build_passing = True
                addon.last_successful_build = right_now
                addon.min_python_version, addon.max_python_version = self.get_python_range(data['matrix'])
                addon.min_django_version, addon.max_django_version = self.get_django_range(data['matrix'])
            else:
                addon.build_passing = False
            addon.save()
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
                Q(auth_digest=auth) | Q(auth_digest='') | Q(auth_digest__isnull=True),
                repo_slug=slug
            )

            # See note above
            if not addon.auth_digest:
                addon.auth_digest = auth    # Save deferred

        except Addon.DoesNotExist:
            pass

        self.process_data(addon, self.get_data(request))

        return HttpResponse(status=200)

    def get(self, request, *args, **kwargs):
        """Just for easier testing."""
        return TemplateResponse(request,
            'aldryn_essential_addons_dashboard/url_ok.html', {})
