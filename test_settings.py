#!/usr/bin/env python
# -*- coding: utf-8 -*-

HELPER_SETTINGS = {
    'ROOT_URLCONF': 'aldryn_essential_addons_dashboard.tests.urls',
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
    ),
    'INSTALLED_APPS': [
        'aldryn_boilerplates',
        'aldryn_essential_addons_dashboard',
        'versionfield',
        'south',
    ],
    'STATICFILES_FINDERS': [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        # important! place right before django.contrib.staticfiles.finders.AppDirectoriesFinder
        'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ],
    'TEMPLATE_LOADERS': [
        'django.template.loaders.filesystem.Loader',
        # important! place right before django.template.loaders.app_directories.Loader
        'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
        'django.template.loaders.app_directories.Loader',
    ],
    'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_essential_addons_dashboard')

if __name__ == "__main__":
    run()
