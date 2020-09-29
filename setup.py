#!/usr/bin/env python
import os

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(HERE, 'insilicodatabase', '__version__.py')) as f:
    exec(f.read(), version)


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='insilico-database',
    version=version['__version__'],
    description="Database for the ligands molecular properties",
    long_description=readme + '\n\n',
    author="Felipe Zapata",
    author_email='f.zapata@esciencecenter.nl',
    url='https://github.com/nlesc-nano/insilico-database',
    packages=[
        'insilicodatabase'
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='insilico-database',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['pandas', 'pymongo', 'pyyaml>=5.1.1'],
    data_files=[('citation/insilicodatabase', ['CITATION.cff'])],
    extras_require={
        'test': ['coverage', 'mypy', 'pycodestyle', 'pytest>=3.9', 'pytest-cov'
                 ],
        'doc': ['sphinx', 'sphinx-autodoc-typehints', 'sphinx_rtd_theme',
                'nbsphinx']
    }

)
