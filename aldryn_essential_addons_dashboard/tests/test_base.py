# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random
import string

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, TransactionTestCase

from cms.models import Title
from cms.utils.i18n import get_language_list
from djangocms_helper.utils import create_user

from ..models import Addon, Dependency

User = get_user_model()


class TestUtilityMixin(object):
    """Just adds some common test utilities to the testing class."""
    def rand_str(prefix='', length=16, chars=string.ascii_letters):
        return '{0}{1}'.format(
            prefix,
            ''.join(random.choice(chars) for _ in range(length))
        )

    def create_addon(self, **kwargs):
        fields = {
            'name': self.rand_str(),
            'repo_slug': self.rand_str(),
        }

        fields.update(**kwargs)
        return Addon.objects.create(**fields)


class CMSRequestBasedTest(TestUtilityMixin, TransactionTestCase):
    """Sets-up User(s) and CMS Pages for testing."""
    languages = get_language_list()

    @classmethod
    def setUpClass(cls):
        cls.request_factory = RequestFactory()
        # if not User.objects.filter(username='normal').count():
        cls.user = create_user('normal', 'normal@admin.com', 'normal')
        cls.site1 = Site.objects.get(pk=1)

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def get_or_create_page(self, base_title=None, languages=None):
        """Creates a page with a given title, or, if it already exists, just
        retrieves and returns it."""
        from cms.api import create_page, create_title
        if not base_title:
            # No title? Create one.
            base_title = self.rand_str(prefix="page", length=8)
        if not languages:
            # If no langs supplied, use'em all
            languages = self.languages
        # If there is already a page with this title, just return it.
        try:
            page_title = Title.objects.get(title=base_title)
            return page_title.page.get_draft_object()
        except:
            pass

        # No? Okay, create one.
        page = create_page(base_title, 'fullwidth.html', language=languages[0])
        # If there are multiple languages, create the translations
        if len(languages) > 1:
            for lang in languages[1:]:
                title_lang = "{0}-{1}".format(base_title, lang)
                create_title(language=lang, title=title_lang, page=page)
                page.publish(lang)
        return page.get_draft_object()

    def get_page_request(self, page, user, path=None, edit=False,
            lang_code='en', method="get", **extra):
        method = method.lower()
        if method not in ['get', 'post', ]:
            raise ImproperlyConfigured(
                'get_page_request() can only do GET or POST requests')
        from cms.middleware.toolbar import ToolbarMiddleware
        path = path or page and page.get_absolute_url()
        if edit:
            path += '?edit'

        if method == 'get':
            request = RequestFactory().get(path, **extra)
        else:
            request = RequestFactory().post(path, **extra)
        request.session = {}
        request.user = user
        request.LANGUAGE_CODE = lang_code
        if edit:
            request.GET = {'edit': None}
        else:
            request.GET = {'edit_off': None}
        request.current_page = page
        mid = ToolbarMiddleware()
        mid.process_request(request)
        return request
