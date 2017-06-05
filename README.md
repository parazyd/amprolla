amprolla
========

<img src="contrib/amprolla.png" width="64">

amprolla is an apt repository merger originally intended for use with
the [Devuan](https://devuan.org) infrastructure. This version is the
third iteration of the software. The original version of amprolla was
not performing well in terms of speed, and the second version was never
finished - therefore this version has emerged.


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

Edit `lib/config.py` to your needs, and then run `amprolla_init.py`.
This will download the repositories we will merge afterwards. When this
is done, you can now run `amprolla_merge.py` which will perform the
merge, and finally sign the Release files needed.

A `nginx` configuration for the amprolla server can be found in
`contrib`.

More information on amprolla should be found in the `doc` directory.
