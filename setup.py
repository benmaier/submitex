from setuptools import setup, Extension
import setuptools
import os
import sys

# get __version__, __author__, and __email__
exec(open("./submitex/metadata.py").read())

setup(
    name='submitex',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url='https://github.com/benmaier/submitex',
    license=__license__,
    description=r"Tools and CLIs to make your tex-files submission-ready.",
    long_description='',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
    ],
    tests_require=['pytest', 'pytest-cov'],
    setup_requires=['pytest-runner'],
    classifiers=['License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.11',
                 'Programming Language :: Python :: 3.12',
                 ],
    project_urls={
        'Documentation': 'http://submitex.benmaier.org',
        'Contributing Statement': 'https://github.com/benmaier/submitex/blob/master/CONTRIBUTING.md',
        'Bug Reports': 'https://github.com/benmaier/submitex/issues',
        'Source': 'https://github.com/benmaier/submitex/',
        'PyPI': 'https://pypi.org/project/submitex/',
    },
    entry_points = {
          'console_scripts': [
                  'resolvepipes = submitex.resolvepipes:cli',
                  'replacebib = submitex.replacebib:cli',
                  'replacefigs = submitex.replacefigs:cli',
                  'resolveinputs = submitex.resolveinputs:cli',
                  'collectfloats = submitex.collectfloats:cli',
                  'removecomments = submitex.removecomments:cli',
              ],
        },
    include_package_data=True,
    zip_safe=False,
)
