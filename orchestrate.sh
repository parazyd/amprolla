#!/bin/sh
# See LICENSE file for copyright and license details.

# Orchestration of incremental updates

# Make sure these correlate to lib/config.py
AMPROLLA_UPDATE="${AMPROLLA_UPDATE:-/home/amprolla/amprolla/amprolla_update.py}"
REPO_ROOT="${REPO_ROOT:-/home/amprolla/amprolla}"
AMPROLLA_LOCK="/run/lock/amprolla.lock"
RSYNC_URL="mirror@pkgmaster.devuan.org:/home/mirror/"

[ -f "${AMPROLLA_LOCK}" ] || {

[ -d "${REPO_ROOT}/merged-staging" ] || mkdir "${REPO_ROOT}/merged-staging"
[ -d "${REPO_ROOT}/merged-production" ] || mkdir "${REPO_ROOT}/merged-production"


ln -snf "$REPO_ROOT"/merged-staging "$REPO_ROOT"/merged
# The break call is temporary to catch unhandled exceptions in the testing phase
python3 "$AMPROLLA_UPDATE" || {
	ln -snf "$REPO_ROOT"/merged-production "$REPO_ROOT"/merged
}

printf "rsyncing volatile to production... "
rsync --delete -raX "$REPO_ROOT"/merged-volatile/* "$REPO_ROOT"/merged-production
echo "done!"

ln -snf "$REPO_ROOT"/merged-production "$REPO_ROOT"/merged

printf "rsyncing volatile to staging... "
rsync --delete -raX "$REPO_ROOT"/merged-volatile/* "$REPO_ROOT"/merged-staging
echo "done!"

printf "rsyncing production to pkgmaster... "
rsync --delete -raX \
	"$REPO_ROOT"/merged-production/ "${RSYNC_URL}/merged"
echo "done!"

# handle obsolete package logs
cat "$REPO_ROOT"/log/*-oldpackages.txt | sort | uniq > "$REPO_ROOT"/log/oldpackages.txt

_logfiles="libsystemd bannedpackages"
mkdir -p "$REPO_ROOT"/log/t
for i in $_logfiles; do
	sort "$REPO_ROOT/log/${i}.txt" | uniq > "$REPO_ROOT/log/t/${i}.txt"
done
cp -f "$REPO_ROOT"/log/t/*.txt "$REPO_ROOT"/log/

rsync "$REPO_ROOT"/log/t/*.txt ${RSYNC_URL}
rsync "$REPO_ROOT"/log/oldpackages.txt "$REPO_ROOT"/log/amprolla.txt ${RSYNC_URL}
}
