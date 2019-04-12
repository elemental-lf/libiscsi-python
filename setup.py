#!/usr/bin/env python3
import os
import os.path
import shutil
import subprocess
import sys

try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext
    from setuptools.command.build_py import build_py
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext
    from distutils.command.build_py import build_py

libiscsi_git_url = 'https://github.com/sahlberg/libiscsi'
libiscsi_release = '1.18.0'
long_description = open('README.md').read()

cwd = os.getcwd()
libiscsi_build_env = 'libiscsi-{}/build-env'.format(libiscsi_release)
libiscsi_src = 'libiscsi-{}/src'.format(libiscsi_release)
libiscsi_install_root = 'libiscsi-{}/install-root'.format(libiscsi_release)
# Make this path absolute for configure
libiscsi_install_root = os.path.abspath(libiscsi_install_root)
libiscsi_swig = 'libiscsi-{}/swig'.format(libiscsi_release)
libiscsi_swig_c_files = ['libiscsi_wrap.c']
libiscsi_swig_py_files = ['libiscsi.py']
#libiscsi_c_flags = '-fPIC -Wimplicit-fallthrough=0 -Werror=format-truncation=0'
libiscsi_c_flags = '-fPIC -w'
libiscsi_configure_flags = ['--prefix={}'.format(libiscsi_install_root), '--disable-shared']


class BuildExtLibISCSI(build_ext):

    @staticmethod
    def libiscsi_git_clone_libiscsi():
        if not os.path.exists(libiscsi_src):
            subprocess.run(['git', 'clone', libiscsi_git_url, libiscsi_src],
                           stdout=sys.stdout,
                           stderr=sys.stderr,
                           check=True,
                           env=os.environ)

    @staticmethod
    def libiscsi_git_checkout_libiscsi():
        os.chdir(libiscsi_src)
        subprocess.run(['git', 'checkout', libiscsi_release],
                       stdout=sys.stdout,
                       stderr=sys.stderr,
                       check=True,
                       env=os.environ)
        os.chdir(cwd)

    @staticmethod
    def libiscsi_copy_build_env():
        for base, dirs, files in os.walk(libiscsi_build_env):
            for f in files:
                src = os.path.join(base, f)
                dst = os.path.join(libiscsi_src, os.path.relpath(base, start=libiscsi_build_env), f)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
                shutil.copystat(src, dst)

    @staticmethod
    def libiscsi_configure_libiscsi():
        subprocess_env = {'CFLAGS': libiscsi_c_flags}

        os.chdir(libiscsi_src)
        subprocess.run(
            ['./configure'] + libiscsi_configure_flags,
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=True,
            env=dict(list(os.environ.items()) + list(subprocess_env.items())))
        os.chdir(cwd)

    @staticmethod
    def libiscsi_install_libiscsi():
        os.chdir(libiscsi_src)
        subprocess.run(['make', 'install'], stdout=sys.stdout, stderr=sys.stderr, check=True, env=os.environ)
        os.chdir(cwd)

    @staticmethod
    def libiscsi_copy_swig_c_files():
        for file in libiscsi_swig_c_files:
            src = '{}/{}'.format(libiscsi_swig, file)
            dst = 'libiscsi/{}'.format(file)
            shutil.copyfile(src, dst)
            shutil.copystat(src, dst)

    def run(self):
        self.libiscsi_git_clone_libiscsi()
        self.libiscsi_git_checkout_libiscsi()
        self.libiscsi_copy_build_env()
        self.libiscsi_configure_libiscsi()
        self.libiscsi_install_libiscsi()
        self.libiscsi_copy_swig_c_files()
        super().run()


class BuildPyLibISCSI(build_py):

    @staticmethod
    def libiscsi_copy_swig_py_files():
        for file in libiscsi_swig_py_files:
            src = '{}/{}'.format(libiscsi_swig, file)
            dst = 'libiscsi/{}'.format(file)
            shutil.copyfile(src, dst)
            shutil.copystat(src, dst)

    def run(self):
        self.libiscsi_copy_swig_py_files()
        super().run()


_libiscsi = Extension(
    name='libiscsi._libiscsi',
    sources=['libiscsi/libiscsi_wrap.c'],
    libraries=['iscsi'],
    library_dirs=[os.path.join(cwd, 'libiscsi-{}/install-root/lib'.format(libiscsi_release))],
    include_dirs=[os.path.join(cwd, 'libiscsi-{}/install-root/include'.format(libiscsi_release))],
)

setup(
    name='libiscsi',
    version='1.0.post1',
    description='A libiscsi wrapper for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='LGPLv2.1',
    platforms=['any'],
    author='Ronnie Sahlberg, Lars Fenneberg',
    author_email='ronniesahlberg@gmail.com, lf@elemental.net',
    url='https://github.com/elemental-lf/libiscsi-python/',
    packages=['libiscsi'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    ext_modules=[_libiscsi],
    cmdclass={
        'build_ext': BuildExtLibISCSI,
        'build_py': BuildPyLibISCSI
    })
