# Compatibility for us old-timers.
PHONY=check clean dist distclean test rmChangeLog

# Note: This makefile include remake-style target comments.
# These comments before the targets start with #:
# remake --tasks to shows the targets and the comments

PHONY=check check-short  clean dist distclean test lint

GIT2CL ?= git2cl
BASH ?= bash
PYTHON ?= python
PYTHON3 ?= python3

#: the default target - same as running "check"
all: check

#: style and warning check
lint:
	flake8 pyficache

PHONY=check clean dist distclean test rmChangeLog

#: the default target - same as running "check"
all: check

#: Same as "check"
test: check

#: Same as "check-short"
test-short: check-short

#: Run all tests - the pytest way
check:
	$(PYTHON) -m pytest test

#: Clean up temporary files
#: Clean up temporary files and .pyc files
clean: clean_pyc
	$(PYTHON) ./setup.py $@
	find . -name __pycache__ -exec rm -fr {} \; || true
	(cd test && $(MAKE) clean)
	(cd test_unit && $(MAKE) clean)

#: Remove .pyc files
clean_pyc:
	$(RM) -f */*.pyc */*/*.pyc || true

#: Run coverage
coverage:
	coverage

#: Create source (tarball) and binary (egg) distribution
dist:
	${BASH} ./admin-tools/make-dist-newest.sh

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
	patch -p0 < ChangeLog-spell-corrected.diff

rmChangeLog:
	rm ChangeLog || true

.PHONY: $(PHONY)
