#!/bin/bash

FILENAME="$1"

if [ -z "$FILENAME" -o ! -f "$FILENAME" ]; then
	echo >&2 "Missing GitHub stars json filename."
	exit 2
fi

for row in $(jq -c '.[] | {name, url}' "$FILENAME"); do
	NAME="$(echo "$row" | jq -r '.name')"
	URL="$(echo "$row" | jq -r '.url')"

	git clone -j4 -n --recursive "$URL" "$NAME"
done
