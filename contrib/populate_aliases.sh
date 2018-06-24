#!/bin/sh
# See LICENSE file for copyright and license details.

# Helper script to be ran once after the initial mass merge in
# order to populate the structure with the needed symlinks.

dryrun=""
[ "$1" = "-d" ] && dryrun="echo"

# make sure these correlate to lib/config.py
REPO_ROOT="${REPO_ROOT:-/srv/amprolla/merged}"

PAIRS="
	jessie                   1.0
	jessie                   oldstable
	jessie-backports         oldstable-backports
	jessie-proposed-updates  oldstable-proposed-updates
	jessie-security          oldstable-security
	jessie-updates           oldstable-updates

	ascii                    2.0
	ascii                    stable
	ascii-backports          stable-backports
	ascii-proposed-updates   stable-proposed-updates
	ascii-security           stable-security
	ascii-updates            stable-updates

	beowulf                  3.0
	beowulf                  testing
	beowulf-backports        testing-backports
	beowulf-proposed-updates testing-proposed-updates
	beowulf-security         testing-security
	beowulf-updates          testing-updates

	unstable                 ceres
"

$dryrun cd "$REPO_ROOT" || exit 1

echo "$PAIRS" | while read -r codename suite; do
	if [ -n "$codename" ] && [ -n "$suite" ]; then
		if echo "$codename" | grep -qv '^#'; then
			$dryrun ln -snfv "$codename" "$suite"
		fi
	fi
done
