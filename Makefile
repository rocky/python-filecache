# Compatibility for us old-timers.
PHONY=check clean dist distclean test rmChangeLog

# Note: This makefile include remake-style target comments. 
# These comments before the targets start with #:
# remake --tasks to shows the targets and the comments

GIT2CL ?= git2cl
PYTHON ?= python
PYTHON3 ?= python3

PHONY=check clean dist distclean test rmChangeLog

#: the default target - same as running "check"
all: check

#: Same as "check" 
test: check

#: Same as "check-short" 
test-short: check-short

#: Run all tests
check: 
	$(PYTHON) ./setup.py nosetests
	[[ $(PYTHON3) != $(PYTHON) ]] && $(PYTHON3) ./setup.py nosetests || true

#: Run unit (white-box) tests
check-short: 
	$(PYTHON) ./setup.py nosetests --quiet | \
	$(PYTHON) ./make-check-filter.py

#: Clean up temporary files
clean: 
	$(PYTHON) ./setup.py $@

#: Create source (tarball) and binary (egg) distribution
dist: 
	$(PYTHON) ./setup.py sdist bdist_egg

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
