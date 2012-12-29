# Compatibility for us old-timers.

# Note: This makefile include remake-style target comments. 
# These comments before the targets start with #:
# remake --tasks to shows the targets and the comments

PHONY=check clean dist distclean test
all: check

#: Run all tests
check: 
	python ./setup.py nosetests

#: Clean up temporary files
clean: 
	python ./setup.py $@


#: Create source (tarball) and binary (egg) distribution
dist: 
	python ./setup.py sdist bdist

# It is too much work to figure out how to add a new command to distutils
# to do the following. I'm sure distutils will someday get there.
DISTCLEAN_FILES = build dist *.egg-info *.pyc *.so

#: Remove ALL dervied files 
distclean: clean
	-rm -fr $(DISTCLEAN_FILES) || true

#: Install package locally
install: 
	python ./setup.py install

#: Same as 'check' target
test: check


#: Create a ChangeLog from SVN via svn2cl
ChangeLog:
	svn2cl --authors=svn2cl_usermap http://pyficache.googlecode.com/svn/trunk -o $@

.PHONY: $(PHONY)
