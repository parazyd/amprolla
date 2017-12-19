#!/bin/sh
# See LICENSE file for copyright and license details.

# Orchestration of incremental updates

# Make sure these correlate to lib/config.py
AMPROLLA_UPDATE="${AMPROLLA_UPDATE:-/home/amprolla/amprolla/amprolla_update.py}"
REPO_ROOT="${REPO_ROOT:-/home/amprolla/amprolla}"

[ -f "/run/lock/amprolla.lock" ] || {
ln -snf "$REPO_ROOT"/merged-staging "$REPO_ROOT"/merged
# The break call is temporary to catch unhandled exceptions in the testing phase
python3 "$AMPROLLA_UPDATE" || {
	ln -snf "$REPO_ROOT"/merged-production "$REPO_ROOT"/merged
}

printf "rsyncing volatile to production... "
rsync --delete -raX "$REPO_ROOT"/merged-volatile/* "$REPO_ROOT"/merged-production
printf "done!\n"

ln -snf "$REPO_ROOT"/merged-production "$REPO_ROOT"/merged

printf "rsyncing volatile to staging... "
rsync --delete -raX "$REPO_ROOT"/merged-volatile/* "$REPO_ROOT"/merged-staging
printf "done!\n"

printf "rsyncing production to pkgmaster... "
rsync --delete -raX \
	"$REPO_ROOT"/merged-production/ \
	mirror@pkgmaster.devuan.org:/home/mirror/devuan/merged
printf "done!\n"

# handle obsolete package logs
cat "$REPO_ROOT"/log/*-oldpackages.txt | sort | uniq > "$REPO_ROOT"/log/oldpackages.txt

_logfiles="libsystemd bannedpackages"
mkdir -p "$REPO_ROOT"/log/t
for i in $_logfiles; do
	sort "$REPO_ROOT"/log/${i}.txt | uniq > "$REPO_ROOT"/log/t/${i}.txt
done
cp -f "$REPO_ROOT"/log/t/*.txt "$REPO_ROOT"/log/

rsync "$REPO_ROOT"/log/t/*.txt mirror@pkgmaster.devuan.org:/home/mirror/devuan/
rsync "$REPO_ROOT"/log/oldpackages.txt "$REPO_ROOT"/log/amprolla.txt \
	mirror@pkgmaster.devuan.org:/home/mirror/devuan/
}
