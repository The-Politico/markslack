from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='markslack',
    version='0.0.0-alpha',
    description='A Slack message format to Markdown converter',
    long_description=long_description,
    url='https://github.com/The-Politico/markslack',
    author='Jon McClure',
    author_email='jon.r.mcclure@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='slack markdown',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['emoji'],

    extras_require={
        'test': ['pytest'],
    },
)
