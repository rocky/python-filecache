git pull

# Change version in VERSION.py

    $ emacs pyficache/VERSION.py
    $ source pyficache/VERSION.py
    $ echo $VERSION
    $ git commit -m"Get ready for release $VERSION" .


# Update ChangeLog:

    $ make ChangeLog

#  Update NEWS from ChangeLog. Then:

    $ emacs NEWS
    $ make check
    $ git commit --amend .
    $ git push   # get CI testing going early
    $ make check

# Make sure pyenv is running and check newer versions

    $ pyenv local && source admin-tools/check-newer-versions.sh

# Switch to python-2.4, sync that up and build that first since it creates a tarball which we don't want.

    $ source admin-tools/setup-python-2.4.sh
    $ git merge master

# Update NEWS from master branch

    $ git commit -m"Get ready for release $VERSION" .

# Check against all versions

    $ bash && echo $SHLVL # Go into a subshell to protect exit
    $ source admin-tools/check-older-versions.sh
    $ source admin-tools/check-newer-versions.sh
	$ echo $SHLVL ; exit

# Make packages and tag

    $ . ./admin-tools/make-dist-older.sh
    $ git tag release-python-2.4-$VERSION

    $ . ./admin-tools/make-dist-newer.sh
    $ git tag release-$VERSION

# Upload single package and look at Rst Formating

    $ twine upload dist/pyficache-${VERSION}-py3.3.egg

# Upload rest of versions

    $ twine upload dist/pyficache-${VERSION}*

# Push tags:

    $ git push --tags

# Check on a VM

    $ cd /virtual/vagrant/virtual/vagrant/ubuntu-zesty
	$ vagrant up
	$ vagrant ssh
	$ pyenv local 3.5.2
	$ pip install --upgrade pyficache
	$ exit
	$ vagrant halt
