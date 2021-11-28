#!/bin/bash
PYTHON_VERSION=3.1.5

owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..

(cd ../python-xdis && git checkout python-3.1-to-3.2 && pyenv local $PYTHON_VERSION) && git pull && \
    pyenv local $PYTHON_VERSION

cd $owd
git checkout python-3.1-to-3.2
rm -v */.python-version || true
