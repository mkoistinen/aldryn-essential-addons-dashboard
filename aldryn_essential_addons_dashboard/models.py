# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from versionfield import VersionField


@python_2_unicode_compatible
class Dependency(models.Model):

    addon = models.ForeignKey('aldryn_essential_addons_dashboard.Addon',
        verbose_name=_('addon'), blank=False, default=None, related_name='addon')
    dependency = models.ForeignKey('aldryn_essential_addons_dashboard.Addon',
        verbose_name=_('dependency'), blank=False, default=None, related_name='dependency')
    optional = models.BooleanField(_('optional dependency?'), default=False)

    class Meta:
        verbose_name = _('dependency')
        verbose_name_plural = _('dependencies')

    def __str__(self):
        return self.pk


@python_2_unicode_compatible
class Addon(models.Model):

    name = models.CharField(_('name'), max_length=255, blank=False, default='',
        help_text=_('Can be anything but should be the official addon name.'))

    repo_slug = models.CharField(max_length=255, blank=False, default='',
        unique=True, help_text=_('This <b>must</b> match the GitHub repo '
        'account/name. E.g., "divio/django-cms".'))

    auth_digest = models.CharField(max_length=64, blank=True, editable=False)

    open_source = models.BooleanField(default=False,
        help_text=_('Check this box if the addon’s repo is open sourced.'))

    published = models.BooleanField(default=False,
        help_text=_('Check this box if the addon is published in the Aldryn '
                    'Addon Marketplace.'))

    version = VersionField(verbose_name=_('version'), blank=True,
        help_text=_('This will be populated automatically.'))

    # These store the latest /successfully tested/ versions of Python/Django
    max_python_version = VersionField(verbose_name=_('max. Python version'),
        blank=True, null=True,
        help_text=_('This will be populated automatically.'))

    max_django_version = VersionField(verbose_name=_('max. Django version'),
        blank=True, null=True,
        help_text=_('This will be populated automatically.'))

    build_passing = models.BooleanField(_('build passing?'), default='False',
        help_text=_('This will be populated automatically.'))

    dependencies = models.ManyToManyField('self', blank=True,
        verbose_name=_('dependencies'), through='Dependency',
        symmetrical=False, related_name='component_of')

    class Meta:
        verbose_name = _('addon')
        verbose_name_plural = _('addons')

    def __str__(self):
        return self.name
