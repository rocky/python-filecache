#!/bin/bash
PYTHON_VERSION=3.8

export PATH=$HOME/.pyenv/bin/pyenv:$PATH
setup_filecache_owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..

(cd ../python-xdis && git checkout master && pyenv local $PYTHON_VERSION) && git pull && \
    git checkout master && git pull && pyenv local $PYTHON_VERSION
cd $setup_filecache_owd
rm -v */.python-version || true
