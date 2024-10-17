#/bin/bash
# Setup for running Python 2.4 .. 2.7, merging python-3.1-to-3.2 into this branch
pyfilecache_merge_24_owd=$(pwd)
cd $(dirname ${BASH_SOURCE[0]})
if . ./setup-python-2.4.sh; then
    git merge python-3.0-to-3.2
fi
cd $pyfilecache_merge_24_owd
