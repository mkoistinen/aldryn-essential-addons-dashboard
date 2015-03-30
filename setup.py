# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_essential_addons_dashboard import __version__

REQUIREMENTS = [
    'aldryn-boilerplates',
    'django-versionfield3',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn_essential_addons_dashboard',
    version=__version__,
    description='Live development status of Aldryn Essential Addons',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-essential-addons-dashboard',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
