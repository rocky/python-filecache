#!/bin/bash
PYTHON_VERSION=2.4.6

if [[ $0 == $${BASH_SOURCE[0]} ]] ; then
    echo "This script should be *sourced* rather than run directly through bash"
    exit 1
fi

(cd ../python-xdis && git checkout python-2.4 && pyenv local $PYTHON_VERSION) && git pull && \
    git checkout python-2.4  && git pull && pyenv local $PYTHON_VERSION
