# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from hashlib import sha256

from .models import Addon, Dependency


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
        return super(
            DependencyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class AddonAdminForm(forms.ModelForm):
    token = forms.CharField(max_length=100, required=False,
        widget=forms.widgets.PasswordInput(),
        help_text=_('This should be the Travis token for the account that '
                    'originally setup this repo.'))

    class Meta:
        fields = [
            'name', 'repo_slug', 'token', 'open_source', 'published',
            'version', 'max_python_version', 'max_django_version',
            'build_passing'
        ]

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
    list_display = ('name', 'version', 'max_python_version',
        'max_django_version', 'build_passing', 'published', 'open_source', )
    inlines = (DependencyAdmin, )
    ordering = ('name', )
    # list_editable = ('build_passing', 'published', 'open_source', )

    def get_formsets(self, request, obj=None):
        """
        Only show the DependencyAdmin in the change form, not the add form.
        """
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, DependencyAdmin) and obj is None:
                continue
            yield inline.get_formset(request, obj)


admin.site.register(Addon, AddonAdmin)
