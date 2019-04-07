# libiscsi-python

This module is an iSCSI client for Python 3.  It is hosted at
https://github.com/elemental-lf/libiscsi-python and is a fork of
https://github.com/sahlberg/libiscsi-python.  It adds a few things things to
make this module actually usable to read and write data.

In addition it comes with a complete build environment and does not require 
installation of `swig`, `autoconf`, `automake` or `libtool`. It builds `libiscsi`
from  source and links the extension module with the resulting library, no system
installation of `libiscsi` is required. The only thing that is required is
a working C compiler installation.

The build process required Internet access to download the `libiscsi` sources.

## LICENSE

This module is distributed under LGPL version 2.1.  Please see COPYING for
the full text of this license.
