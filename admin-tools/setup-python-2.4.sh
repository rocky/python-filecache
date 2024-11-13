#!/bin/bash
PYTHON_VERSION=2.4

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
cd $fulldir/..

(cd $fulldir/.. && setup_version python-xdis python-2.4 && \
    setup_version shell-term-background python-2.4
    )

cd $python_filecache_owd
rm -v */.python-version 2>/dev/null || true
checkout_finish python-2.4-to-2.7
