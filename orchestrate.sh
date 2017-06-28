#!/bin/sh
# orchestration of incremental updates

# make sure these correlate to lib/config.py
AMPROLLA_UPDATE=/srv/amprolla/amprolla_update.py
REPO_ROOT=/srv/amprolla

# TODO: remove the while loop and run with cron after testing phase

while true; do
	ln -snf "$REPO_ROOT"/merged-staging "$REPO_ROOT"/merged
	# the break call is temporary to catch unhandled exceptions in the testing phase
	python3 "$AMPROLLA_UPDATE" || break
	printf "rsyncing volatile to production...\n"
	rsync --delete -raX "$REPO_ROOT"/merged-volatile/* "$REPO_ROOT"/merged-production
	printf "done!\n"
	ln -snf "$REPO_ROOT"/merged-production "$REPO_ROOT"/merged
	printf "rsyncing volatile to staging...\n"
	rsync --delete -raX "$REPO_ROOT"/merged-volatile/* "$REPO_ROOT"/merged-staging
	printf "done!\n"
	sleep 3600
done
