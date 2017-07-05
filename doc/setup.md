amprolla setup
==============

amprolla should be able to run on any system supporting Python 3, rsync
and GnuPG. However it has only been tested on Devuan and Gentoo.


Installation
------------

The recommended way to install Python 3 and the needded modules, along
with the extra needed dependencies is using your package manager.

You will need the following:

```
python3, python-gnupg, python-requests, gnupg2, rsync
```

After installing the required dependencies, clone the amprolla git repo
using git to a place of your preference.

You will also need to setup a valid gnupg directory structure, along with
a key you shall use for signing the Release files if you require to do so.


Configuration
-------------

To configure amprolla, a default configuration file is provided in
`lib/config.def.py`. Copy the file to `lib/config.py` and edit it to
your needs. The configuration file contains all the information needed
to properly merge the required repositories. The default configuration
is also working as long as you provide a valid gpg fingerprint used to
sign the Release files. If you do not wish to sign Release file, make
sure to disable it in the configuration file.

The `*dir` variables in the configuration file are the directories
where the files that are being merged are kept and the merges itself
are done. They can be either absolute or relative paths to the root
amprolla directory. The prefered way is to actually have absolute paths
as this will cause less trouble.

`banpkgs` is a set of package names that amprolla will refuse to merge
if they are found either in the dependencies of a package or if they
are the package itself.

`repo_order` is a list that holds that is ordered in the priority the
packages are prefered. The preference is ordered first to last.
The dict `repos` itself holds the required information for them.

### repos dict structure

* The variable is a normal dict where the key is a string that should
  be contained in `repo_order`. They key's values are another dict with
  the following fields:

	- `name`: the name of the repository used for rewriting the path to
	  the package's upstream (deb file). It is used in the nginx config
	  provided in the `contrib` directory.

	- `host`: the upstream URL where the repository is being held. Used
	  to know from where to download the necessary Packages/Release files
	  and how to rewrite certain values.

	- `dists`: the root directory where the suites are held. It is appended
	  to the above URL.

	- `aliases`: if True, when downloading/rewriting, will look for the
	  suite's alias defined later in the configuration file.

	- `skipmissing`: a hack helpful to skip missing suites if the repo
	  we are merging does not contain them.


`suites` hold our release names and their suites.

`aliases` hold the suites we want to merge as aliases in case we know a
certain repository doesn't use the same name for it.

`release_aliases` list our stable and testing branch aliases.

`categories` hold the package categories we wish to actually merge. apt
repositories usually hold `main`, `contrib`, and `non-free`. With this
we can opt out of any of them.

`arches` list the actual architectures we want to merge. If we are not
using certain architectures, it is easy to exclude them from merging
this way.

It is advised to not touch any variables listed below these, as they
are currently setup to provide a correct (valid) apt repository.


Running amprolla
----------------

After you've setup amprolla, it is needed to perform the initial full
download and full merge. First run `amprolla_init.py`, which is going
to download the necessary directory structures (as defined through the
config file) we will merge afterwards. When the download is done, it is
time to perform the full initial merge of these repositories. This will
provide us with a complete merged repository and we will then be able
to easily perform incremental updates of it.

After the first merge has been performed, it is advisable to run a
script called `populate_aliases.sh` found in the `contrib` directory.
Make sure you edit it and set a proper path to your merged directory,
and fill out the proper names needed. It will populate the merged
directory with symlinks to certain versions such as `1.0`, `stable`, or
`testing`.

Incremental updates are performed through `amprolla_update.py`, however,
for more stable performance and uptime, the incremental updating is
being orchestrated by a shell script called `orchestrate.sh`. This shell
script holds the logic to have near-atomic switching of repositories to
minimize repo downtime during performed merges. Not doing this could
result with users downloading corrupted repository files if they are
requested during an ongoing merge.

In a screen/tmux session, simply execute the `orchestrate.sh` script
and it will start looping and doing incremental updates every hour.
If you prefer, you can remove this loop and run the shell script through
a cron job based on your needs.

To actually serve the merged directory over HTTP, a basic nginx
configuration is provided as `contrib/nginx.conf`.
