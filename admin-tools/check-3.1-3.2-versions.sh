#!/bin/bash
function finish {
  cd $filecache_check_31_owd
}
filecache_check_31_owd=$(pwd)
trap finish EXIT

cd $(dirname ${BASH_SOURCE[0]})
if ! source ./pyenv-3.1-3.2-versions ; then
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
cd $filecache_check_31_owd
