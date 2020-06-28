<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Get latest sources:](#get-latest-sources)
- [Change version in version.py](#change-version-in-versionpy)
- [Update ChangeLog:](#update-changelog)
- [Update NEWS from ChangeLog. Then:](#update-news-from-changelog-then)
- [Make sure pyenv is running and check newer versions](#make-sure-pyenv-is-running-and-check-newer-versions)
- [Switch to python-2.4, sync that up and build that first since it creates a tarball which we don't want.](#switch-to-python-24-sync-that-up-and-build-that-first-since-it-creates-a-tarball-which-we-dont-want)
- [Update NEWS from master branch. Then..](#update-news-from-master-branch-then)
- [Check against all versions](#check-against-all-versions)
- [Make packages and tag](#make-packages-and-tag)
- [Release on Github](#release-on-github)
- [Get on PyPy](#get-on-pypy)
- [Push tags:](#push-tags)
- [Move dist files to uploaded](#move-dist-files-to-uploaded)

<!-- markdown-toc end -->

# Get latest sources:

    git pull

# Change version in version.py

    $ emacs pyficache/version.py
    $ source pyficache/version.py
    $ echo $VERSION
    $ git commit -m"Get ready for release $VERSION" .


# Update ChangeLog:

    $ make ChangeLog

#  Update NEWS from ChangeLog. Then:

    $ emacs NEWS.md
    $ make check
    $ git commit --amend .
    $ git push   # get CI testing going early
    $ make check

# Make sure pyenv is running and check newer versions

    $ pyenv local && source admin-tools/check-newer-versions.sh

# Switch to python-2.4, sync that up and build that first since it creates a tarball which we don't want.

    $ source admin-tools/setup-python-2.4.sh
    $ git merge master

# Update NEWS from master branch. Then..

    $ git commit -m"Get ready for release $VERSION" .
    $ git push origin HEAD

# Check against all versions

    $ bash && echo $SHLVL # Go into a subshell to protect exit
    $ source admin-tools/check-older-versions.sh
    $ source admin-tools/check-newer-versions.sh
	$ echo $SHLVL ; exit

# Make packages, check, and tag

    $ . ./admin-tools/make-dist-older.sh
	$ pyenv local 3.8.3
	$ twine check dist/pyficache-$VERSION*
    $ git tag release-python-2.4-$VERSION
    $ . ./admin-tools/make-dist-newer.sh
	$ twine check dist/xdis-$VERSION*

# Release on Github

Goto https://github.com/rocky/python-filecache/releases/new

Set version, copy in `NEWS.md` item, upload binaries.

Now check the *tagged* release. (Checking the untagged release was previously done).

Todo: turn this into a script in `admin-tools`

	$ pushd /tmp/gittest
	$ pip install -e git://github.com/rocky/python-filecache@$VERSION.git#egg=pyficache
	$ pip uninstall pyficache
	$ popd


	$ twine check dist/pyficache-$VERSION*

# Get on PyPI

	$ twine upload dist/pyficache-${VERSION}*

Check on https://pypi.org/project/pyficache/

# Push and Pull tags:

    $ git push --tags
    $ git pull --tags

# Move dist files to uploaded

	$ mv -v dist/xdis-${VERSION}* dist/uploaded
