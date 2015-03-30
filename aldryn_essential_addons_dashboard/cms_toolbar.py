# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from .models import Addon


@toolbar_pool.register
class AddonsToolbar(CMSToolbar):
    watch_models = (Addon, )

    def populate(self):
        if self.request.user.has_perm(
                'aldryn_essential_addons_dashboard.change_addon'):

            view_name = self.request.resolver_match.view_name
            is_detail_view = (
                view_name == 'aldryn_essential_addons_dashboard:addon-detail')
            is_list_view = (
                view_name == 'aldryn_essential_addons_dashboard:addon-list')

            if is_detail_view or is_list_view:
                menu = self.toolbar.get_or_create_menu(
                    'aldryn-essential-addons-dashboard-app-menu', _('Addons'))

                if self.request.user.has_perm(
                        'aldryn_essential_addons_dashboard.change_addon'):
                    menu.add_sideframe_item(_('Addon list'), url=admin_reverse(
                        'aldryn_essential_addons_dashboard_addon_changelist'))

                if self.request.user.has_perm(
                        'aldryn_essential_addons_dashboard.add_addon'):
                    menu.add_modal_item(_('Add new addon'), url=admin_reverse(
                        'aldryn_essential_addons_dashboard_addon_add'))

                if is_detail_view:
                    slug = self.request.resolver_match.kwargs['slug']
                    addons = Addon.objects.filter(slug=slug)
                    if addons.count() == 1:
                        menu.add_modal_item(_('Edit addon'), url=admin_reverse(
                            'aldryn_essential_addons_dashboard_addon_change',
                            args=(addons[0].pk,)
                        ), active=True,)
