2.1.0 2018-01-26
================

This shifts responsibility of getting line offset info to `xdis`. But we have routines here
since we manage file objects and cache them.

To this end routines `code_lines()` and and `code_line_info()` were added.

Line information now contains all offsets for a given line number in
the module or function that the offset is relative to. There are various options
for indicting whether you want the offset informaiton or just the line numbers,
nnd if you want to note which line numbers are dups.

2.0.0 2018-01-26
================

* We remove dependency on coverage which was writing .coverage files. Fixes #25
  A dependency on xdis was added, but that's okay since that allows handling
  cross-version bytecode which is a good thing
* `py2pyc()` renamed to `resolve_name_to_path()`, and use `importlib` to help
  use resolve names if that is available. This is why we need to bump from 1.0 to 2.0
* blacken some buffers and regularize imports

1.0.1 2018-04-16
=================

- Pygments needs to be 1.4 on Python 2.4 branch.

1.0.0 2018-01-26
================

With this release, we use semantic versioning. There is
some API incompatiablity with the last release, and old
compatibility routines have been removed

- Redo the way file to file line remapping works. The API changes here
- unamp_file_line has a reverse option to indicate which way to map/unmap
- remove older compatibility routine cache()

0.3.2 2017-07-03
================

- Extend back to Python 2.4 via branch python-2.4
- Small administrative changes

0.3.1 2017-07-01 python-2.4
===========================

- Python 2.3 -2.5 tolerance

0.3.1 2016-11-12
================

- Be able to distinguish files without EOL
  Changes due to and thanks to John Vandenberg
  See https://github.com/coala/coala-bears/issues/815

0.3.0 2015-11-29 John
=====================

- Allow setting a pygments style and other pygments options.  Requires pygments 2.x
- Some bugs fixed and doc updated.

0.2.6 2015-04-15
================

- Fix bug in `update_script_cache()`
- Minor changes for testing and travis

0.2.5 2015-04-15
================

- Add remove_remap_file() which will be used in trepanning debuggers
- Modernize somewhat: revise doc and __init__.py to use rSt.

0.2.4 2015-03-24
================

- First github release

0.2.3 2013-03-24
=================

- Python 2.5 compatibility

0.2.2 2013-02-10
=================

- Make it work on 3k

0.2.1 2013-01-06
================

- Handle "dark" and "light" terminal style
- Remove a Coverage warning
- Fix bug in clearing file cache

0.2.0 2013-01-01
================

- Caches terminal syntax-colorized code for terminals
- Interface more closely matches Ruby linecache module.
- Treats filename.pyc like filename.py

0.1.4 2010-10-28
================

- Correct packaging

0.1.3 2009-03-15
================

- incorrect "Provide" in setup.cfg

0.1.2 2009-03-15 - Ron Frankel Release
======================================

- Bug in searching for files

0.1.0 2009-03-08 - Ron Frankel -1 Release
=========================================

- Initial release
