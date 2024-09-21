#!/bin/bash
# Check out master branch and dependent development master branches
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

PYTHON_VERSION=3.12

mydir=$(dirname $bs)
pyficache_owd=$(pwd)
cd $mydir
. ./checkout_common.sh
fulldir=$(readlink -f $mydir)
cd $fulldir/..

(cd ../python-xdis && git checkout master && pyenv local $PYTHON_VERSION) && \
    git checkout master && git pull && pyenv local $PYTHON_VERSION
cd $python_filecache_owd
rm -v */.python-version || true
checkout_finish master
