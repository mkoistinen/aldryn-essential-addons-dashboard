# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import re
import warnings

from django.conf import settings
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, View
from django.utils.timezone import now

from versionfield.version import Version
from versionfield.constants import DEFAULT_NUMBER_BITS as DEFAULT_BITS

from .models import Addon, PostLog

ZERO = Version('0.0.0', DEFAULT_BITS)
MAX  = Version('255.255.65535', DEFAULT_BITS)

DEBUG_POST = getattr(settings, 'ESSENTIAL_ADDONS_DASHBOARD_DEBUG_POST', False)


class AddonListView(ListView):
    http_method_names = ['get', ]
    model = Addon


class AddonDetailView(DetailView):
    http_method_names = ['get', ]
    model = Addon


class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)


class WebhookViewBaseView(CsrfExemptMixin, View):
    http_method_names = ['post', 'get']
    post_log = []
    payload_name = 'payload'
    service_name = '[unnamed service]'

    _json_data_cache = None

    def log(self, log_type, msg):
        log_type = log_type.upper()
        if log_type not in ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']:
            raise ValueError('Unknown log log_type: {0}'.format(log_type))
        self.post_log.append('[{log_type}] {msg}\n'.format(
            log_type=log_type, msg=msg))

    def is_authentic(self, request, addon):
        self.log('WARN', 'Using default is_authentic(), failed authentication.')
        return False

    def write_log(self):
        """Writes the log to the database."""
        if getattr(settings, 'ESSENTIAL_ADDONS_DASHBOARD_DEBUG_POST', False):
            try:
                PostLog.objects.create(
                    details="".join(self.post_log),
                    log_timestamp=now()
                )
            except:
                # We never want the logging to interrupt the reponse back to
                # the service.
                warnings.warn('Could not write log!')

    def dispatch(self, request, *args, **kwargs):
        """Do some header logging."""
        self.post_log = []
        self._json_data_cache = None
        self.log('INFO', 'Received post from {0} @ {1}'.format(
            self.service_name, now()))
        for h, v in request.META.iteritems():
            if h.startswith('HTTP_') or h in [
                    'CONTENT_LENGTH', 'CONTENT_TYPE', ]:
                self.log('INFO', 'Found header: {0}:{1}'.format(h, v))
        return super(WebhookViewBaseView, self).dispatch(
            request, *args, **kwargs)

    def get_json_data(self, request):
        """
        Returns the JSON payload from the request. It is memoised since it may
        be called more than once, but won't ever change in the same request.
        """
        if not self._json_data_cache:
            payload = request.POST.get(self.payload_name, None)
            if payload:
                self._json_data_cache = json.loads(payload) if payload else []
            else:
                self._json_data_cache = None
                self.log('WARN', 'get_json_data() found no data in request.')

        return self._json_data_cache

    def process_data(self, request, data):
        """Must be implemented"""
        msg = 'WebhookViews must implement a process_data() method.'
        self.log('ERROR', msg)
        raise NotImplementedError(msg)

    def get_addon(self, request, data):
        """Must be implemented"""
        msg = 'WebhookViews must implement a get_addon() method.'
        self.log('ERROR', msg)
        raise NotImplementedError(msg)

    def post(self, request, *args, **kwargs):
        """Primary entry point for the service webhook."""
        addon = self.get_addon(request)
        if addon:
            self.log('INFO', 'Found addon: {0}'.format(addon))
            if not self.is_authentic(request, addon):
                self.log('WARN', 'Did not authenticate for addon: {0}.'.format(addon))
                self.write_log()
                return HttpResponse('', status=401)

            self.process_data(addon, self.get_json_data(request))
        else:
            self.log('WARN', 'No addon found.')

        self.write_log()
        return HttpResponse('', status=200)

    def get(self, request, *args, **kwargs):
        """Provides a human-friendly view of the endpoint with instruction."""
        url = request.build_absolute_uri()
        return TemplateResponse(request,
            'aldryn_essential_addons_dashboard/url_ok.html', {
                'service': self.service_name,
                'webhook_url': url,
                'config_example': """
                    ...
                    notifications:
                    webhooks: {0}
                    ...
                """.format(url)
            })


class HeaderMixinBase(object):

    def format_header(self, header):
        """
        Returns a properly formatted header name for Django. Namely, that it is
        in all caps, uses underscores, not dashes and is prefixed with 'HTTP_'.
        """
        new_header = header.upper().replace('-', '_')
        if not new_header.startswith('HTTP_'):
            new_header = 'HTTP_' + new_header
        return new_header


class AddonFromHeaderMixin(HeaderMixinBase):
    addon_slug_header = ''
    addon_slug_field = 'repo_slug'

    def __init__(self, *args, **kwargs):
        self.addon_slug_header = self.format_header(self.addon_slug_header)
        return super(AddonFromHeaderMixin, self).__init__(*args, **kwargs)

    def get_addon(self, request):
        """Returns the addon that is the target of this notification."""
        slug = request.META.get(self.addon_slug_header, None)
        if slug:
            try:
                return Addon.objects.get(**{self.addon_slug_field: slug})
            except Addon.DoesNotExist:
                self.log('WARN', 'Addon "{0}" not found.'.format(slug))
                return None

        self.log('WARN', 'Addon_slug_header: {0} not found!'.format(
            self.addon_slug_header))
        return None


class HeaderAuthenticationMixin(HeaderMixinBase):
    auth_header = ''
    addon_auth_digest_field = 'auth_digest'

    def __init__(self, *args, **kwargs):
        self.auth_header = self.format_header(self.auth_header)
        return super(HeaderAuthenticationMixin, self).__init__(*args, **kwargs)

    def is_authentic(self, request, addon):
        """
        Given the found addon, attempt to authenticate the request. If the
        addon's auth_digest is currently empty, we'll store one found here and
        future posts will have to match this one to be accepted.
        """
        self.log('DEBUG', 'Is_authentic() is Looking for header: "{0}"'.format(
            self.auth_header))
        if addon:
            auth = request.META.get(self.auth_header, None)
            if auth:
                addon_value = getattr(addon, self.addon_auth_digest_field, None)
                if hasattr(addon, self.addon_auth_digest_field):
                    if addon_value == auth:
                        return True
                else:
                    # OK, this is the first time we've seen this service, let's
                    # store the auth code supplied now.
                    setattr(addon, self.addon_auth_digest_field, auth)
                    # We're deferring the write until later
                    self.log(
                        'WARN',
                        'Initialized auth-digest on addon: "{0}"'.format(addon)
                    )
                    return True
            else:
                self.log('WARN', 'Authorization header: "{0}" not found'.format(
                    self.auth_header))
        return False


class TravisWebhookView(AddonFromHeaderMixin, HeaderAuthenticationMixin, WebhookViewBaseView):
    service_name = 'TravisCI'
    payload_name = 'payload'
    auth_header = 'Authorization'
    addon_auth_digest_field = 'auth_digest'
    addon_slug_header = 'Travis-Repo-Slug'
    addon_slug_field = 'repo_slug'

    def is_authentic(self, request, addon):
        self.log('WARN', 'Bypassing authentication!')
        return True

    def get_job_python(self, job):
        """
        Given a single 'job' object, return the found Python.
        Returns a Version object or None
        """
        if 'config' in job and 'python' in job['config']:
            # json may convert '1.6' into a float, force a string.
            return Version(str(job['config']['python']), DEFAULT_BITS)
        if DEBUG_POST:
            job_id = job['id'] if 'id' in job else "[No ID found]"
            self.log('WARN', 'get_job_python() found no config in job: {0}.'.format(job_id))
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
                        max_python = Version(str(job_python), DEFAULT_BITS)
                    if int(job_python) < int(min_python):
                        min_python = Version(str(job_python), DEFAULT_BITS)
        if max_python == ZERO or min_python == MAX:
            return (None, None)
        return (min_python, max_python)

    def get_job_django(self, job):
        """
        Given a single 'job' object, return the found Django. This one is a bit
        trickier as we'll have to parse it out of the ENV.

        Returns a Version object or None
        """
        job_id = job['id'] if 'id' in job else "[No ID found]"
        pattern = re.compile('.*?django *=[^\d]*(?P<version>[0-9][0-9.]*).*?', re.I)
        if 'config' in job and job['config'] and 'env' in job['config']:
            match = re.match(pattern, job['config']['env'])
            if match:
                ver_num = match.groups('django')[0]
                ver_obj = None

                try:
                    ver_num = int(ver_num)
                    # OK, this is an int, probably something like 14 for 1.4,
                    # etc. so, let's just divide by 10 and call it a day.
                    ver_obj = Version(str(ver_num / 10), DEFAULT_BITS)
                except:
                    pass

                if not ver_obj:
                    # Not an integer, try float
                    try:
                        _ = float(ver_num)
                        # Nice, a float, well, we can use the string version
                        ver_obj = Version(ver_num, DEFAULT_BITS)
                    except:
                        pass

                if not ver_obj:
                    # Hmmm, not float either...
                    try:
                        ver_obj = Version(ver_num, DEFAULT_BITS)
                    except:
                        # Can't say we didn't try
                        self.log('WARN',
                            'Unable to save django version {0} from '
                            'job: {1}'.format(ver_num, job_id))
                        ver_obj = None

                return ver_obj

            else:
                re.match(
                    'TOX_ENV *=.*dj(?P<version>\d+)',
                    job['config']['env'],
                    re.I)
                if match:
                    ver_obj = None
                    try:
                        ver_num = int(ver_num)
                        # OK, this is an int, probably something like 14 for 1.4,
                        # etc. so, let's just divide by 10 and call it a day.
                        ver_obj = Version(str(ver_num / 10), DEFAULT_BITS)
                    except:
                        pass
                return ver_obj
            self.log('WARN', 'get_job_django() found no config in job: {0}.'.format(job_id))

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
                        max_django = Version(str(job_django), DEFAULT_BITS)
                    if int(job_django) < int(min_django):
                        min_django = Version(str(job_django), DEFAULT_BITS)
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
                self.log('INFO', 'Repo builds!')
            else:
                self.log('INFO', 'Repo not building.')
                addon.build_passing = False
            addon.save()
        return


class GitHubWebhookView(HeaderAuthenticationMixin, WebhookViewBaseView):
    service_name = 'GitHub'
    payload_name = 'payload'
    addon_slug_field = 'repo_slug'

    def is_authentic(self, request, addon):
        self.log('WARN', 'Bypassing authentication!')
        return True

    def get_addon(self, request):
        data = self.get_json_data(request)
        if data and 'repository' in data and 'full_name' in data['repository']:
            slug = data['repository']['full_name']
            self.log('INFO', 'Found addon: {0} in data!'.format(slug))
            try:
                return Addon.objects.get(repo_slug=slug)
            except Addon.DoesNotExist:
                self.log('WARN', 'Addon "{0}" not found.'.format(slug))
                return None
        self.log('WARN', 'Unable to find addon slug in data.')
        return None

    def process_data(self, addon, data):
        right_now = now()
        if addon and data:
            if ('ref_type' in data and
                    data['ref_type'] == 'tag' and 'ref' in data):
                tag_name = data['ref']
                try:
                    addon.version = Version(tag_name, DEFAULT_BITS)
                except:
                    self.log(
                        'ERROR',
                        'Unable to determine version from tag_name'.format(
                            tag_name)
                    )
                addon.last_webhook_timestamp = right_now
                self.log('INFO', 'Got version: {0}'.format(tag_name))
            else:
                self.log('WARN', 'Unknown event type from GitHub')
            addon.save()
