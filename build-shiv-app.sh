#!/usr/bin/env bash

# exit if any command returns non zero
set -e

# The directory path of sync-script (the one this file is in)
SS_DPATH=$(dirname $(readlink -f $0))

# clean old build
rm -rf $SS_DPATH/dist $SS_DPATH/trilsync.pyz

pip install -r  <(pipenv lock -r) --target $SS_DPATH/dist

# specify which files to be included in the build
# You probably want to specify what goes here
cp -r \
-t $SS_DPATH/dist \
$SS_DPATH/trilsync

# finally, build!
shiv --site-packages $SS_DPATH/dist --compile-pyc --compressed -p '/usr/bin/env python3.6' -o $SS_DPATH/trilsync.pyz -e 'trilsync.cli:cli'
echo "trilsync.pyz built"
