# Compatibility for us old-timers.
PHONY=check clean dist distclean test rmChangeLog

# Note: This makefile include remake-style target comments.
# These comments before the targets start with #:
# remake --tasks to shows the targets and the comments

PHONY=check check-short  clean dist distclean test lint

GIT2CL ?= git2cl
PYTHON ?= python
PYTHON3 ?= python3

#: the default target - same as running "check"
all: check

#: style and warning check
lint:
	flake8 pyficache.py

PHONY=check clean dist distclean test rmChangeLog

#: the default target - same as running "check"
all: check

#: Same as "check"
test: check

#: Same as "check-short"
test-short: check-short

#: Run all tests
check:
	nosetests

#: Run unit (white-box) tests
check-short:
	$(PYTHON) ./setup.py nosetests --quiet | \
	$(PYTHON) ./make-check-filter.py

#: Clean up temporary files
clean:
	$(PYTHON) ./setup.py $@

#: Run all tests
coverage:
	coverage

#: Create source (tarball) and binary (egg) distribution
dist:
	$(PYTHON) ./setup.py sdist bdist_egg

#: Create source tarball
sdist: README.rst
	$(PYTHON) ./setup.py sdist

#: Create binary egg distribution
bdist_egg:
	$(PYTHON) ./setup.py bdist_egg

# It is too much work to figure out how to add a new command to distutils
# to do the following. I'm sure distutils will someday get there.
DISTCLEAN_FILES = build dist *.egg-info *.pyc *.so py*.py

#: Remove ALL derived files
distclean: clean
	-rm -fr $(DISTCLEAN_FILES) || true

#: Install package locally
install:
	$(PYTHON) ./setup.py install

ChangeLog: rmChangeLog
	git log --pretty --numstat --summary | $(GIT2CL) >$@

rmChangeLog:
	rm ChangeLog || true

.PHONY: $(PHONY)
