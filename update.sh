#!/bin/sh

for d in $(find . -mindepth 2 -maxdepth 2 -type d); do
(
  cd "$d"
  git fetch origin
)
done
