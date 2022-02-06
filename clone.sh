#!/bin/bash

export NJOBS="${NJOBS:-$(nproc)}"

ROOTDIR="$(dirname $0)"
"$ROOTDIR/run.sh" "$@" -- git clone -j '${NJOBS:-1}' -n --recursive '$URL' '$NAME'
