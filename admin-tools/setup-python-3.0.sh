#!/bin/bash
PYTHON_VERSION=3.0

bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
python_filecache_owd=$(pwd)
. ./checkout_common.sh
fulldir=$(readlink -f $mydir)
cd $fulldir/..

(cd $fulldir/.. && setup_version python-xdis python-3.0 && \
    setup_version shell-term-background python-3.0
    )

cd $python_filecache_owd
rm -v */.python-version 2>/dev/null || true
checkout_finish master
