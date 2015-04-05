# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from hashlib import sha256

from .models import Addon, Dependency, PostLog


class PostLogAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(PostLog, PostLogAdmin)


class DependencyAdmin(admin.TabularInline):
    model = Dependency
    fk_name = 'addon'
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dependency":
            try:
                parent_obj_id = request.resolver_match.args[0]
                kwargs["queryset"] = Addon.objects.exclude(id=parent_obj_id)
            except IndexError:
                pass
        return super(DependencyAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class AddonAdminForm(forms.ModelForm):
    token = forms.CharField(max_length=100, required=False,
        widget=forms.widgets.PasswordInput(),
        help_text=_('This should be the Travis token for the account that '
                    'originally setup this repo.'))

    def save(self, commit=True):
        cleaned_data = super(AddonAdminForm, self).clean()
        token = cleaned_data.get('token')
        repo_slug = cleaned_data.get('repo_slug')
        if token and repo_slug:
            self.instance.auth_digest = sha256(repo_slug + token).hexdigest()
            print('### Saving hash: {0}'.format(self.instance.auth_digest))
        return super(AddonAdminForm, self).save(commit=commit)


class AddonAdmin(admin.ModelAdmin):
    form = AddonAdminForm
    inlines = (DependencyAdmin, )
    actions = ['reset_addons', ]
    list_display = (
        'name', 'version',
        # 'featured', 'build_passing', 'published', 'open_source',
    )
    # list_editable = ('featured', 'published', 'open_source', )
    readonly_fields = ('last_successful_build', 'last_webhook_timestamp', )
    ordering = ('name', )

    fieldsets = [
        (None, {
            'fields': [
                'name',
                'repo_slug',
                'featured',
                ('open_source', 'published', ),
                'version',
            ]
        }),
        (_('Advanced'), {
            'classes': ['collapse', ],
            'fields': [
                'token',
                ('min_python_version', 'max_python_version', ),
                ('min_django_version', 'max_django_version', ),
                'build_passing',
                'last_successful_build',
                'last_webhook_timestamp',
            ]
        }),
    ]

    def reset_addons(self, request, queryset):
        rows_updated = queryset.update(
            auth_digest='',
            min_python_version=None,
            max_python_version=None,
            min_django_version=None,
            max_django_version=None,
            build_passing=False,
            last_successful_build=None,
            last_webhook_timestamp=None,
        )
        if rows_updated == 1:
            message_bit = "1 addon was"
        else:
            message_bit = "%s addons were" % rows_updated
        self.message_user(request, "%s successfully reset." % message_bit)
    reset_addons.short_description = "Reset selected addons"

    def get_formsets(self, request, obj=None):
        """
        Only show the DependencyAdmin in the change form, not the add form.
        """
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, DependencyAdmin) and obj is None:
                continue
            yield inline.get_formset(request, obj)


admin.site.register(Addon, AddonAdmin)
