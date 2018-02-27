#!/usr/bin/env bash
set -x
export PYTHONPATH=$PWD:$PYTHONPATH
# get alphatwirl from master branch
pip install -U git+https://github.com/alphatwirl/alphatwirl.git

make install
