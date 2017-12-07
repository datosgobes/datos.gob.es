# Copyright (C) 2017 Entidad P�blica Empresarial Red.es
# 
# This file is part of "ckanext-dge-dashboard (datos.gob.es)".
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
from setuptools import setup, find_packages  # Always prefer setuptools over distutils

setup(
    name='ckanext-dge-dashboard',
    version='1.0.0',
    description='',
    url='http://datos.gob.es',
    author='',
    author_email='',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 2.7',
    ],


    # What does your project relate to?
    keywords='''CKAN dashboard dge''',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=[],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    include_package_data=True,
    package_data={
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points='''
        [ckan.plugins]
        dge_dashboard=ckanext.dge_dashboard.plugin:DgeDashboardPlugin
        
        [paste.paster_command]
        dge_dashboard_initdb = ckanext.dge_dashboard.commands.dge_dashboard:DgeDashboardInitDBCommand
        dge_dashboard_load = ckanext.dge_dashboard.commands.dge_dashboard:DgeDashboardLoadCommand
        dge_dashboard_json = ckanext.dge_dashboard.commands.dge_dashboard:DgeDashboardJsonCommand
        dge_dashboard_csv = ckanext.dge_dashboard.commands.dge_dashboard:DgeDashboardCsvCommand

    	[babel.extractors]
	    ckan = ckan.lib.extract:extract_ckan
    ''',

    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
