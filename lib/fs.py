#!/usr/bin/env python
# copyright (c) 2017 - Ivan J. <parazyd@dyne.org>
# see LICENSE file for copyright and license details

import config


def crawl():
    paths = {}
    for i in range(0, len(config.repos)):
        repo = config.repos[i]["name"]
        basepath = config.repos[i]["dists"]
        sts = []
        for j in config.suites:
            for k in config.suites[j]:
                if config.repos[i]["aliases"] is True:
                    if repo in config.aliases:
                        try:
                            suite = config.aliases[repo][k]
                        except:
                            if config.repos[i]["skipmissing"] is True:
                                continue
                            else:
                                suite = k
                else:
                    suite = k
                skips = ["jessie-security", "ascii-security"]  # XXX: HACK:
                if repo == "DEBIAN" and suite in skips:
                    continue
                sts.append(suite)
        paths[repo] = sts
    return paths

# print(crawl())
