#!/bin/sh

usage() {
	echo >&2 "Usage: $0 -f stars.json [-s repo-name/to-stop-at] -- [... commands to eval...]"
	exit 1
}

while true ; do
    case "$1" in
        -f|--file) FILENAME="$2" ; shift 2 ;;
        -s|--stop-at-name) STOP_NAME="$2" ; shift 2 ;;
        -h|--help) usage ;;
        --) shift ; break ;;
        *) echo >&2 "> Invalid option '$1'" ; usage ;;
    esac
done

if [ -z "$FILENAME" -o ! -f "$FILENAME" ]; then
	echo >&2 "> Missing GitHub stars json filename."
	exit 2
fi

for row in $(jq -c '.[] | {name, url}' "$FILENAME"); do
	NAME="$(echo "$row" | jq -r '.name')"
	URL="$(echo "$row" | jq -r '.url')"

	echo "# $NAME"
	if [ -n "$STOP_NAME" -a "$NAME" = "$STOP_NAME" ]; then
		break
	fi

	(
		eval "$@"
	)
done
