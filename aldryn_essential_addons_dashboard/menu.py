# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import Addon


class AddonMenu(CMSAttachMenu):
    name = _('Aldryn Essential Addons')

    def get_nodes(self, request):
        # nodes = [
        #     NavigationNode(
        #         'List',
        #         reverse('aldryn_essential_addons_dashboard:addon-list'),
        #         'addon-list'
        #     ),
        #     NavigationNode('----', '', ''),
        # ]
        nodes = []

        for addon in Addon.objects.all():
            node = NavigationNode(
                addon.name,
                addon.get_absolute_url(),
                addon.slug,
            )
            nodes.append(node)
        return nodes

menu_pool.register_menu(AddonMenu)
