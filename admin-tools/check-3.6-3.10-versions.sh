#!/bin/bash
function finish {
  cd $filecache_check_36
}
filecache_check_36=$(pwd)
trap finish EXIT

cd $(dirname ${BASH_SOURCE[0]})
if ! source ./pyenv-3.6-3.10-versions ; then
    exit $?
fi
if ! source ./setup-python-3.6.sh ; then
    exit $?
fi

cd ..
for version in $PYVERSIONS; do
    if ! pyenv local $version ; then
	exit $?
    fi
    make clean && python setup.py develop
<<<<<<< HEAD
    if ! make check ; then
=======
    if ! make check-nosetests ; then
>>>>>>> python-3.1-to-3.2
	exit $?
    fi
done
