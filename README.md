amprolla
========

<img src="contrib/amprolla.png" width="64">

amprolla is an apt repository merger originally intended for use with
the [Devuan](https://devuan.org) infrastructure. This version is the
third iteration of the software. The original version of amprolla was
not performing well in terms of speed, and the second version was never
finished - therefore this version has emerged.

amprolla is a tool that will merge a number of different apt-based
repositories into one, while giving control over (not) including given
packages, architectures, or any specific package metadata. Upon completing
the merge, amprolla will generate and optionally create GnuPG signatures
of the according `Release` files.


Dependencies
------------

amprolla requires at least Python 3.4, and some external modules for it.

### Devuan/Debian

```
rsync gnupg2 python3-requests python3-gnupg
```

### Gentoo:

```
net-misc/rsync app-crypt/gnupg dev-python/requests dev-python/python-gnupg
```


Basic usage
-----------

Copy `lib/config.def.py` to `lib/config.py` and edit `lib/config.py` to
your needs, and then run `amprolla_init.py`. This will download the
repositories we will merge afterwards. When this is done, you can run
`amprolla_merge.py` which will perform the actual merge, and finally
sign the Release files needed. The first time this is done, it is
advisable to run the script found in `contrib/populate_aliases.sh` so
it can fill in the needed symlinks to the different suites. Make sure
you set the correct path in the script.

To perform incremental updates, run `orchestrate.sh` with a cron job
in your desired intervals. Edit the script to set the correct paths.

**NOTE:** in the current testing phase, `orchestrate.sh` contains a while
loop in order to be ran in tmux to catch unhandled exceptions and fix
the codebase.

An `nginx` configuration for the amprolla server can be found in
`contrib`.

More documentation should be found in the `doc` directory.
