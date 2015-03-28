# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

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


class AddonAdmin(admin.ModelAdmin):
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
