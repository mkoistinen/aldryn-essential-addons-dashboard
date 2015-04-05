# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_client import forms


class Form(forms.BaseForm):

    enable_post_logging = forms.CheckboxField(
        "enable_post_logging",
        required=False,
        initial=False,
        help_text="You probably don't want to check this."
    )

    disable_csrf_middleware = forms.CheckboxField(
        "disable_csrf_middleware",
        required=False,
        initial=False,
        help_text="Do this only as a last resort!"
    )

    def to_settings(self, cleaned_data, settings_dict):
        if cleaned_data['enable_post_logging']:
            settings_dict['ESSENTIAL_ADDONS_DASHBOARD_DEBUG_POST'] = True

        if cleaned_data['disable_csrf_middleware']:
            # Remove's the CSRF middleware
            if 'MIDDLEWARE_CLASSES' in settings_dict:
                new_mws = []
                for mw in settings_dict['MIDDLEWARE_CLASSES']:
                    if mw != 'django.middleware.csrf.CsrfViewMiddleware':
                        new_mws.append(mw)
                settings_dict['MIDDLEWARE_CLASSES'] = tuple(new_mws)

        return settings_dict
