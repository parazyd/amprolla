#!/bin/sh
set -e

pkg="https://cdn-aws.deb.debian.org/debian/dists/sid/CAT/binary-ARCH/Packages.gz"
src="https://cdn-aws.deb.debian.org/debian/dists/sid/CAT/source/Sources.gz"

case "$1" in
	sources)
		for i in main contrib non-free; do
			url="$(echo "$src" | sed -e "s/CAT/$i/")"
			wget -qO- "$url" | gunzip | grep ': ' | cut -d ':' -f1
		done | sort | uniq
		;;
	packages)
		for i in main contrib non-free; do
			for j in all amd64 i386 arm64 armhf; do
				url="$(echo "$pkg" | sed -e "s/CAT/$i/" -e "s/ARCH/$j/")"
				wget -qO- "$url" | gunzip | grep ': ' | cut -d ':' -f1
			done
		done | sort | uniq
		;;
esac
