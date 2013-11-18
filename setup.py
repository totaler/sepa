# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='sepa',
    version='0.0.1-dev',
    url='',
    author='Grup El Gas, S.A.',
    author_email='informatica@el-gas.es',
    packages=['sepa'],
    requires=['libComXML'],
    license='GPLv3',
    description='SEPA',
    long_description=open('README').read(),
)
