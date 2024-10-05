#!/bin/bash
# Check out master branch and dependent development master branches
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

PYTHON_VERSION=3.12

function checkout_version {
    local repo=$1
    version=${2:-python-3.12}
    echo Checking out $version on $repo ...
    (cd ../$repo && git checkout $version && pyenv local $PYTHON_VERSION) && \
	git pull
    return $?
}

mydir=$(dirname $bs)
pyficache_owd=$(pwd)
cd $mydir
. ./checkout_common.sh
fulldir=$(readlink -f $mydir)

(cd $fulldir/.. && checkout_version python-xdis master && \
    checkout_version shell-term-background master && \
    git checkout master \
    )
cd $python_filecache_owd
rm -v */.python-version 2>/dev/null || true
checkout_finish master
