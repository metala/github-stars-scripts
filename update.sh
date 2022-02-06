#!/bin/bash

ROOTDIR="$(dirname $0)"

"$ROOTDIR/run.sh" "$@" -- \
	cd '$NAME' ';' \
	git fetch origin
