# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TransactionTestCase

from .test_base import TestUtilityMixin


class TestAddonsDashboard(TestUtilityMixin, TransactionTestCase):

    def test_create_addon(self):
        addon = None
        try:
            addon = self.create_addon(
                name='Aldryn Newsblog', repo_slug='aldryn/aldryn-newsblog')
        except:
            self.fail('Could not create addon.')

        if addon:
            self.assertEqual(
                addon.slug,
                'aldryn--aldryn-newsblog'
            )

    def test_get_absolute_url(self):
        """Tests that Addon.get_absolute_url() works."""

        addon = self.create_addon(
            name='Aldryn Newsblog', repo_slug='aldryn/aldryn-newsblog')
        try:
            url = addon.get_absolute_url()
        except Exception as e:
            print(e)
            self.fail('Could not get absolute url.')
