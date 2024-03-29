#!/bin/bash
PACKAGE=pyficache

# FIXME put some of the below in a common routine
function finish {
  cd $make_dist_24_filecache_owd
}

make_dist_24_filecache_owd=$(pwd)
cd $(dirname ${BASH_SOURCE[0]})
trap finish EXIT

if ! source ./pyenv-2.4-2.7-versions ; then
    exit $?
fi
if ! source ./setup-python-2.4.sh ; then
    exit $?
fi

cd ..
source $PACKAGE/version.py
echo $__version__

for pyversion in $PYVERSIONS; do
    echo --- $pyversion ---
    if [[ ${pyversion:0:4} == "pypy" ]] ; then
	echo "$pyversion - PyPy does not get special packaging"
	continue
    fi
    if ! pyenv local $pyversion ; then
	exit $?
    fi
    # pip bdist_egg create too-general wheels. So
    # we narrow that by moving the generated wheel.

    # Pick out first two number of version, e.g. 3.5.1 -> 35
    first_two=$(echo $pyversion | cut -d'.' -f 1-2 | sed -e 's/\.//')
    rm -fr build
    python setup.py bdist_egg
done

echo "--- python 2.7 wheel ---"
pyenv local 2.7.18
python setup.py bdist_wheel

python ./setup.py sdist
tarball=dist/${PACKAGE}-${__version__}.tar.gz
if [[ -f $tarball ]]; then
    mv -v $tarball dist/${PACKAGE}_31-${__version__}.tar.gz
fi
finish
