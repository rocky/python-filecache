#!/bin/bash
PYTHON_VERSION=2.4

function checkout_version {
    local repo=$1
    version=${2:-python-2.4}
    echo Checking out $version on $repo ...
    (cd ../$repo && git checkout $version && pyenv local $PYTHON_VERSION) && \
	git pull
    return $?
}

# FIXME put some of the below in a common routine
function finish {
  cd $setup_filecache_24_owd
}

pyenv local $PYTHON_VERSION

setup_filecache_24_owd=$(pwd)
bs=${BASH_SOURCE[0]}
if [[ $0 == $bs ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

mydir=$(dirname $bs)
fulldir=$(readlink -f $mydir)
cd $fulldir/..

(cd ../python-xdis && git checkout python-2.4-to-2.7 && pyenv local $PYTHON_VERSION) && git pull && \
    git checkout python-2.4  && git pull && pyenv local $PYTHON_VERSION

cd $owd
git checkout python-2.4 && git pull && pyenv local $PYTHON_VERSION
rm -v */.python-version || true
