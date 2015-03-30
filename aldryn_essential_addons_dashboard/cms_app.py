# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from .menu import AddonMenu


class AddonsDashboardApp(CMSApp):
    name = _('Aldryn Essential Addons Dashboard')
    urls = ['aldryn_essential_addons_dashboard.urls']
    menus = [AddonMenu, ]
    app_name = 'aldryn_essential_addons_dashboard'

apphook_pool.register(AddonsDashboardApp)
