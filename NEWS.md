2.5.0 2025-09-15
================

Start support for formatting and printing Python disassembly (pyasm) files.
Much more work is needed, but this will probably be good enough for BSidesNYC 2025.

2.4.0 2025-01-15
================

Revised to allow easier line-number remapping.

Note: API change!

`code_line_info` now returns tuple code_map and line numbers


2.3.2 2024-10-16
================

Handle `highlight="plain"` in `getlines()` It needs to override "style"

Lots of little administrative things to support newer Python up to 3.13 while allowing functioning on older Python. For example, `pyproject.toml` was added.


2.3.1 2024-03-15
================

* Adjust for more recent xdis.
* Numerous bug fixes.
* black, isort, and lint files.
* Source code for older Python is now in separate branches.


2.3.0 2021-10-15
================

 Revise to use xdis 6.0.0 - Python version comparisons use tuples instead of floats, which are horribly broken on 3.10.

Some other minor changes as well.

2.2.1 2020-08-30
================

Add the ability to remap filenames by file pattern. Here is a scenario:
I am doing remote debugging so that the files seen by the debugger issuing commands are in a different location than where the core parts of the debugger get run.

While it may be the case that most of the time you expect that
_debugger_, not this module, needs to handle the remap, library routines
here like `add_remap_pat()` and `remap_file_pat()` can be useful.


2.2.0 2020-06-27
================

Uses revised `xdis`. Export `cache_code_lines()` which is needed in the upcoming `trepan3k`
Added  `cache_offset_info()`.

2.1.0 2020-06-12 Fleetwood 66
==============================

This shifts the responsibility of getting line offset info to `xdis`. But we have routines here since we manage file objects and cache them.

To this end routines `code_lines()` and and `code_line_info()` were added.

Line information now contains all offsets for a given line number in the module or function that the offset is relative to. There are various options for indicating whether you want the offset information or just the line numbers, and if you want to note which line numbers are duplicates.

2.0.1 2018-04-22
================

2.0.0's setup.py was missing the package parameter, and this botched the whole release.

2.0.0 2018-04-22
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
some API incompatibility with the last release, and old
compatibility routines have been removed

- Redo the way file-to-file line remapping works. The API changes here
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
- Minor changes for testing and Travis

0.2.5 2015-04-15
================

- Add remove_remap_file(), which will be used in trepanning debuggers
- Modernize somewhat: revise doc and __init__.py to use rSt.

0.2.4 2015-03-24
================

- First GitHub release

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
