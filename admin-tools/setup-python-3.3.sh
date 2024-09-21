#!/bin/bash
PYTHON_VERSION=3.3

function checkout_version {
    local repo=$1
    version=${2:-python-3.3}
    echo Checking out $version on $repo ...
    (cd ../$repo && git checkout $version && pyenv local $PYTHON_VERSION) && \
	git pull
    return $?
}

# FIXME put some of the below in a common routine
function finish {
  cd $setup_filecache_33_owd
}

export PATH=$HOME/.pyenv/bin/pyenv:$PATH
setup_filecache_33_owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
(cd $fulldir/.. && checkout_version python-xdis python-3.3-to-3.5 && checkout_version python-filecache python-3.3-to-3.5)
cd $owd
rm -v */.python-version || true
finish
