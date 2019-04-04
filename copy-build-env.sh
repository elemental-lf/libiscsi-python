#!/bin/bash
LIBISCSI_RELEASE=1.18.0
BUILD_ENV="build-env-$LIBISCSI_RELEASE"

set -euo pipefail

rm -rf "$BUILD_ENV"
mkdir "$BUILD_ENV"
cd libiscsi-lib
./autogen.sh

cp -rv m4 "../$BUILD_ENV"
for file in $(find -name 'Makefile.in' -type f); do
    dir="../$BUILD_ENV/$(dirname $file)"
    [ -d $dir ] || mkdir -p "$dir"
    cp -v "$file" "../$BUILD_ENV/$file"
done

for file in config.h.in ar-lib compile install-sh configure config.sub aclocal.m4 missing config.guess depcomp ltmain.sh; do
    cp -v "$file" "../$BUILD_ENV"
done
