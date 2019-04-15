# libiscsi-python

This module is an iSCSI client for Python 3.  It is hosted at
https://github.com/elemental-lf/libiscsi-python and is a fork of
https://github.com/sahlberg/libiscsi-python.  It adds a few things things to
make this module actually usable to read and write data.

It comes with a build environment and does only require `git`, `make` and a
working C compiler installation. In addition it requires Internet access
to download the `libiscsi` sources. `swig`, `autoconf`, `automake` or `libtool`
are not needed.  It builds `libiscsi` from  source and links the extension
module with the resulting  library, no system installation of `libiscsi` is
required.

## Installation

For RHEL/CentOS 7:

```bash
yum install -y git make gcc epel-release
yum install -y python36
python3 -m venv libiscsi
. libiscsi/bin/activate
pip install git+https://github.com/elemental-lf/libiscsi-python
```

## LICENSE

This module is distributed under LGPL version 2.1.  Please see COPYING for
the full text of this license.
