#!/bin/sh
# helper script to be ran once after the initial mass merge in order
# to populate the structure with the needed symlinks

dryrun=""
[ "$1" = "-d" ] && dryrun="echo"

# make sure these correlate to lib/config.py
REPO_ROOT="/srv/amprolla"

PAIRS="
	jessie                   1.0
	jessie                   stable
	jessie-backports         stable-backports
	jessie-proposed-updates  stable-proposed-updates
	jessie-security          stable-security
	jessie-updates           stable-updates

	ascii                    2.0
	ascii                    testing
	ascii-backports          testing-backports
	ascii-proposed-updates   testing-proposed-updates
	ascii-security           testing-security
	ascii-updates            testing-updates

	unstable                 ceres
"

$dryrun cd "$REPO_ROOT" || exit 1

echo "$PAIRS" | while read codename suite; do
	[ -n "$codename" ] && [ -n "$suite" ] && [ $(echo "$codename" | grep -v '^#') ] && {
		$dryrun ln -snfv "$codename" "$suite"
	} || continue
done
