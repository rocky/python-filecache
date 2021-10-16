#!/bin/bash
PYTHON_VERSION=3.3.7

owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..

(cd ../python-xdis && git checkout python-3.3-3.5 && pyenv local $PYTHON_VERSION) && git pull && \
    pyenv local $PYTHON_VERSION

cd $owd
rm -v */.python-version || true
