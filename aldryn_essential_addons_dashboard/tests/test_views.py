# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..models import Addon, Dependency
from ..views import ProcessTravisWebhookView

from .test_base import CMSRequestBasedTest

from .payload import FAILING_PAYLOAD, PAYLOAD


class TestProcessTravisWebhookView(CMSRequestBasedTest):

    def test_get(self):
        """Tests that a GET to the page will respond with instructions."""
        request = self.get_page_request(
            None, self.user, '/en/addons/', method='get')
        response = ProcessTravisWebhookView.as_view()(request, kwargs={})
        self.assertContains(
            response.render(),
            "Great! This is the correct URL."
        )

    # def test_empty_post(self):
    #     """Tests that a POST to the page works."""
    #     request = self.get_page_request(
    #         None, self.user, '/en/addons/', method='post')
    #     response = ProcessTravisWebhookView.as_view()(request, kwargs={})
    #     self.assertEquals(response.status_code, 200)

    def test_good_build(self):
        addon = self.create_addon(
            name='Aldryn NewsBlog', repo_slug='aldryn/aldryn-newsblog')
        request = self.get_page_request(
            None, self.user, '/en/addons/', method='post', data={
                'payload': PAYLOAD
            }, **{
                'HTTP_TRAVIS_REPO_SLUG': addon.repo_slug
            })
        response = ProcessTravisWebhookView.as_view()(request, kwargs={})
        self.assertEquals(response.status_code, 200)
        addon = Addon.objects.get(pk=addon.pk)

        self.assertEquals(addon.min_python_version, '2.6.0')
        self.assertEquals(addon.max_python_version, '3.5.0')
        self.assertEquals(addon.min_django_version, '1.6.0')
        self.assertEquals(addon.max_django_version, '1.9.0')
        self.assertEquals(addon.build_passing, True)

    def test_bad_build(self):
        addon = self.create_addon(
            name='Aldryn NewsBlog', repo_slug='aldryn/aldryn-newsblog')
        request = self.get_page_request(
            None, self.user, '/en/addons/', method='post', data={
                'payload': FAILING_PAYLOAD
            }, **{
                'HTTP_TRAVIS_REPO_SLUG': addon.repo_slug
            })
        response = ProcessTravisWebhookView.as_view()(request, kwargs={})
        self.assertEquals(response.status_code, 200)
        addon = Addon.objects.get(pk=addon.pk)
        self.assertEquals(addon.build_passing, False)

    def test_bad_headers(self):
        request = self.get_page_request(
            None, self.user, '/en/addons/', method='post', data={
                'payload': FAILING_PAYLOAD
            }, **{
                'HTTP_TRAVIS_REPO_SLUG': 'NOT_A_VALID_REPO_SLUG'
            })
        response = ProcessTravisWebhookView.as_view()(request, kwargs={})
        self.assertEquals(response.status_code, 200)
