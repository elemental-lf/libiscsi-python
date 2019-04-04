#!/usr/bin/env python3
import os
import os.path
import shutil
import subprocess
import sys

try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext
    import setuptools.command.build_py
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext

libiscsi_release = '1.18.0'
long_description = open('README').read()


cwd = os.getcwd()
libiscsi_build_env='build-env-{}'.format(libiscsi_release)
libiscsi_src='libiscsi-src-{}'.format(libiscsi_release)
libiscsi_root='libiscsi-root-{}'.format(libiscsi_release)

class BuildExtLibISCSI(build_ext):
  def _copy_build_env(self):
    for base, dirs, files in os.walk(libiscsi_build_env):
        for f in files:
            src = os.path.join(base, f)
            dst = os.path.join(libiscsi_src, os.path.relpath(base, start=libiscsi_build_env), f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            shutil.copystat(src, dst)
            
  def _configure_libiscsi(self):
    subprocess_env = { 'CFLAGS': '-fPIC -Wimplicit-fallthrough=0 -Werror=format-truncation=0' }
    libiscsi_root_abs = os.path.abspath(libiscsi_root)
    os.chdir(libiscsi_src)
    subprocess.run(['./configure', '--prefix={}'.format(libiscsi_root_abs), '--disable-shared'], stdout=sys.stdout, stderr=sys.stderr, check=True, env=dict(list(os.environ.items()) + list(subprocess_env.items())))
    os.chdir(cwd)
    
  def _install_libiscsi(self):
    os.chdir(libiscsi_src)
    subprocess.run(['make', 'install'], stdout=sys.stdout, stderr=sys.stderr, check=True, env=os.environ)
    os.chdir(cwd)

  def run(self):
    self._copy_build_env()
    self._configure_libiscsi()
    self._install_libiscsi()
    super().run()

_libiscsi = Extension(name='libiscsi._libiscsi',
                      sources=['libiscsi/libiscsi.i'],
                      libraries=['iscsi'],
                      library_dirs=[os.path.join(cwd, 'libiscsi-root-{}/lib'.format(libiscsi_release))],
                      include_dirs=[os.path.join(cwd, 'libiscsi-root-{}/include/iscsi'.format(libiscsi_release))],
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
      cmdclass = {'build_ext': BuildExtLibISCSI}
      )
