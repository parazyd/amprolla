* an older spool directory hierarchy, for testing the merging:
  https://pub.parazyd.cf/tmp/spool.tgz (2GB)


workflow
--------

`amprolla-init` creates the `spool` directory hierarchy. This hierarchy
is the untouched repositories we want to merge. They can be found in
`lib/config.py` in the `repos` dict.

`fs.crawl()` takes the info from `config.py` and generates the paths we
use to figure out what to download. Then `popDirs()` in `amprolla-init`
uses these paths to actually create the directory structure and download
the `Release` files from there. (NOTE: at a final point it should also
check the gpg signatures from the `InRelease` file)

After the Release files are downloaded, they are parsed for their
contents and all the files they list are downloaded in series (possibly
should be parallel).

So now we have all the files we need to create a merge.



The merge will be done in the `merged/` directory. To do a successful
merge, these are the points that need to be accomplished:

	* we must skip packages that are in `config.py/amprolla.banpkgs`
	* for each `binary-$arch` we must create a new `Packages` file,
	  containing our merge:
		* we parse every package and fill in a dict
		* first priority 0, then 1, then 2, etc...
		* if a package already exists from a higher-priority repo - it
		  gets skipped
		* (NOT SURE): if a package from `banpkgs` is in a package's
		  dependency list - that package gets skipped
		* once we've finished the iteration, we dump a new Packages file
		  from the updated dict



After the initial merge, we need to watch for updates. My idea is to
make amprolla pool the above-mentioned Release files as they contain
enough metadata for us to find out what changed. They also contain a
date entry so we can see if there was actually an update without digging
too deep.

So if we figure out there was an update, we download the new file, parse
it into a dict and compare it to the old version of that file/dict.
