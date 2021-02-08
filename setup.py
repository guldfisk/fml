import os

from setuptools import setup


def package_files(directory):
    paths = []
    for path, directories, file_names in os.walk(directory):
        for filename in file_names:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('fml')

setup(
    name = 'fml',
    version = '1.0',
    packages = ['fml'],
    package_data = {'': extra_files},
    dependency_links = [
        'https://github.com/guldfisk/hardcandy/tarball/master#egg=hardcandy-1.0',
        'https://github.com/guldfisk/secretresources/tarball/master#egg=secretresources-1.0',
    ],
    install_requires = [
        'flask',
        'flask-API',
        'requests',
        'sqlalchemy',
        'playsound',
        'py-notifier ',
        'appdirs',
        'hardcandy',
        'secretresources',
        'texttable',
        'gevent',
        'click',
        'gnuplotlib',
        'numpy',
        'alembic',
    ]
)
