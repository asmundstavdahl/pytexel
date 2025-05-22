#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pytexel',
    version='0.1.0',
    description='Pixel graphics as ASCII text art',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='',
    author_email='',
    url='',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    install_requires=[
        'Pillow',
    ],
    extras_require={
        'dev': ['numpy', 'pygame'],
    },
    include_package_data=True,
    package_data={'pytexel': ['ascii.png']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)