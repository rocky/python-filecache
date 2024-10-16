#!/bin/bash
# Setup for running Python 3.3 .. 3.5, merging master into this branch
pyfilecache_33_owd=$(pwd)
cd $(dirname ${BASH_SOURCE[0]})
if . ./setup-python-3.3.sh; then
    git merge python-3.6-to-3.10
fi
cd $pyfilecache_33_owd
