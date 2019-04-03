#!/usr/bin/env python
from os import environ

try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext

long_description = open('README').read()

_libiscsi = Extension(name='libiscsi._libiscsi',
                      sources=['libiscsi/libiscsi.i'],
                      libraries=['iscsi'],
                      library_dirs=['/usr/lib64/iscsi', '/usr/lib/iscsi'],
                      swig_opts=['-py3', '-shadow'],
)


setup(name = 'libiscsi',
      version = '1.0.post1',
      description = 'A libiscsi wrapper for Python.',
      long_description = long_description,
      license = 'LGPLv2.1',
      platforms = ['any'],
      author = 'Ronnie Sahlberg, Lars Fenneberg',
      author_email = 'ronniesahlberg@gmail.com, lf@elemental.net',
      url = 'https://github.com/elemental-lf/libiscsi-python/',
      packages = ['libiscsi'],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: C',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      ext_modules = [_libiscsi],
      )
