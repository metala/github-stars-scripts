#!/bin/bash

FILENAME="$1"
STOP_NAME="$2"
shift 2

NJOBS="${NJOBS:-$(nproc)}"

if [ -z "$FILENAME" -o ! -f "$FILENAME" ]; then
	echo >&2 "Missing GitHub stars json filename."
	exit 2
fi

for row in $(jq -c '.[] | {name, url}' "$FILENAME"); do
	NAME="$(echo "$row" | jq -r '.name')"
	URL="$(echo "$row" | jq -r '.url')"

	echo "# $NAME"
	if [ -n "$STOP_NAME" -a "$NAME" = "$STOP_NAME" ]; then
		break
	fi

	git clone -j "${NJOBS:-1}" -n --recursive "$URL" "$NAME"
done
echo "> End"
