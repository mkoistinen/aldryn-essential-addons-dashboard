# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import re

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from versionfield.version import Version

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

    def get_job_python(self, job):
        """Given a single 'job' object, return the found Python."""
        if job['config'] and job['config']['python']:
            return job['config']['python']
        return None

    def get_max_python_success(self, matrix):
        max_python = Version('0.0.0')
        for job in matrix:
            if job["state"] == "finished" and job["status"] == 0:
                job_python = self.get_job_python(job)
                if job_python and job_python > max_python:
                    max_python = job_python
        if max_python > Version('0.0.0'):
            return max_python
        return None

    def get_job_django(self, job):
        """
        Given a single 'job' object, return the found Django. This one is a bit
        trickier as we'll have to parse it out of the ENV.
        """
        pattern = re.compile('.*?django *= *(?<version>[0-9][0-9.]*).*?', re.I)
        if job['config'] and job['config']['env']:
            grps = re.match(pattern, job['config']['env'])
            if grps:
                return grps.groups['django']
        return None

    def get_max_django_success(self, matrix):
        max_django = Version('0.0.0')
        for job in matrix:
            if job['state'] == 'finished' and job['status'] == 0:
                job_django = self.get_job_django(job)
                if job_django and job_django > max_django:
                    max_django = job_django
        if max_django > Version('0.0.0'):
            return max_django
        return None

    def process_data(self, addon, data):
        if data['matrix']:
            addon.max_python_version = self.get_max_python(data['matrix'])
            addon.max_django_version = self.get_max_django(data['matrix'])
            addon.build_passing = data['matrix']['status'] == 0
            warnings.warn('Updating "{0}" with: {1}, {2}, {3}'.format(
                addon,
                addon.max_python_version,
                addon.max_django_version,
                addon.build_passing,
            ))
            addon.save()

    def post(self, request, *args, **kwargs):
        # TODO: See: http://docs.travis-ci.com/user/notifications/#Authorization-for-Webhooks
        # Too bad the docs provide the wrong headers!
        slug = request.META.get('HTTP_TRAVIS_REPO_SLUG', None)
        auth = request.META.get('HTTP_AUTHORIZATION', None),
        addon = None
        try:
            addon = Addon.objects.get(repo_slug=slug)
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
