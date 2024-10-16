#!/bin/bash
# Check out master branch and dependent development master branches
PYTHON_VERSION=3.13

bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
pyficache_owd=$(pwd)
cd $mydir
. ./checkout_common.sh
fulldir=$(readlink -f $mydir)

(cd $fulldir/.. && setup_version python-xdis master && \
    setup_version shell-term-background master
    )
cd $python_filecache_owd
rm -v */.python-version 2>/dev/null || true
checkout_finish master
