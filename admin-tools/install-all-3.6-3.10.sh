#!/usr/bin/bash
PACKAGE="pyficache"
pyficache_owd=$(pwd)
bs=${BASH_SOURCE[0]}
mydir=$(dirname $bs)
pyficache_fulldir=$(readlink -f $mydir)
cd $pyficache_fulldir

source ../${PACKAGE}/version.py
if [[ ! $__version__ ]] ; then
    echo "Something is wrong: __version__ should have been set."
    exit 1
fi

pyenv_file="pyenv-3.6-3.10-versions"
if ! source $pyenv_file ; then
    echo "Having trouble reading ${pyenv_file} version $(pwd)"
    exit 1
fi

cd ../dist/

install_file="pyficache_36-${__version__}.tar.gz"
for pyversion in $PYVERSIONS; do
    echo "*** Installing ${install_file} for Python ${pyversion} ***"
    pyenv local $pyversion
    pip install $install_file
    python -c 'import pyficache; print(pyficache.__version__)'
    echo "----"
done
