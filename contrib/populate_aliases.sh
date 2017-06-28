#!/bin/sh
# helper script to be ran once after the initial mass merge in order
# to populate the structure with the needed symlinks

# make sure these correlate to lib/config.py
REPO_ROOT=/srv/amprolla

REPOS="
	backports
	proposed-updates
	security
	updates
"

cd "$REPO_ROOT"/merged-volatile/dists

for i in $REPOS; do
	ln -snfv "ascii-$i" "testing-$i"
	ln -snfv "jessie-$i" "stable-$i"
done

ln -snfv "ascii" "testing"
ln -snfv "jessie" "stable"
ln -snfv "unstable" "ceres"
ln -snfv "jessie" "1.0"
ln -snfv "ascii" "2.0"

cd - >/dev/null
