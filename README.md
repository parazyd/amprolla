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

amprolla requires at least Python 3.5, and some external modules for it.

### Devuan Ascii/Debian Stretch

```
gnupg2 python3-requests python3-gnupg
```

### Gentoo:

```
app-crypt/gnupg dev-python/requests dev-python/python-gnupg
```


Basic usage
-----------

Copy `lib/config.def.py` to `lib/config.py` and edit `lib/config.py` to
your needs, and then run `amprolla_init.py`. This will download the
repositories we will merge afterwards. When this is done, you can run
`amprolla_merge.py` which will perform the actual merge, and finally
sign the Release files needed. To perform incremental updates, run
`amprolla_update.py` with a cron job in your desired intervals.

An `nginx` configuration for the amprolla server can be found in
`contrib`.
