#!/bin/bash
function finish {
  cd $filecache_check_33
}
filecache_check_33=$(pwd)
trap finish EXIT

cd $(dirname ${BASH_SOURCE[0]})
if ! source ./pyenv-3.3-3.5-versions ; then
    exit $?
fi
if ! source ./setup-python-3.3.sh ; then
    exit $?
fi

cd ..
for version in $PYVERSIONS; do
    if ! pyenv local $version ; then
	exit $?
    fi
    make clean && python setup.py develop
    if ! make check-nosetests ; then
	exit $?
    fi
done
