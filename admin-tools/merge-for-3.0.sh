#!/bin/bash
# Setup for running Python 3.0 .. 3.2, merging master into this branch
pyfilecache_30_owd=$(pwd)
cd $(dirname ${BASH_SOURCE[0]})
if . ./setup-python-3.0.sh; then
    git merge python-3.3-to-3.5
fi
cd $pyfilecache_30_owd
