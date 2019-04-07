#!/bin/bash
LIBISCSI_RELEASE=1.18.0
SRC="$LIBISCSI_RELEASE/src"

set -euo pipefail

cd "$SRC"
rm -rf "../build-env"
mkdir "../build-env"
./autogen.sh

cp -rv m4 "../build-env"
for file in $(find -name 'Makefile.in' -type f); do
    dir="../build-env/$(dirname $file)"
    [ -d $dir ] || mkdir -p "$dir"
    cp -v "$file" "../build-env/$file"
done

for file in config.h.in ar-lib compile install-sh configure config.sub aclocal.m4 missing config.guess depcomp ltmain.sh; do
    cp -v "$file" "../build-env"
done
