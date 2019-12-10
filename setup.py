from setuptools import setup, find_packages
PACKAGES = find_packages()


NAME = 'Seattle Food Insepctions'
DESCRIPTION = 'Visualization of Seattle food inspection data overlayed with'\
              'local census information.'
URL = 'https://github.com/hyspacex/Seattle-Food-Inspections'
LICENSE = 'MIT'
AUTHOR = 'djclancy, hyspacex, sadrafh, gtalpey'
VERSION = '1.0'
PACKAGE_DATA = {'seattlefoodinspection': ['data/clean_data/*']}
with open('requirements.txt') as f:
    REQUIRES = f.read().splitlines()

opts = dict(name=NAME,
            description=DESCRIPTION,
            url=URL,
            license=LICENSE,
            author=AUTHOR,
            version=VERSION,
            install_requires=REQUIRES
            )


if __name__ == '__main__':
    setup(**opts)
