# -*- coding: utf-8 -*-
#  Copyright (C) 2015 Rocky Bernstein <rocky@gnu.org>
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
|Downloads| |Build Status| |Latest Version| |Supported Python versions|

SYNOPSIS
========

The *pyficache* module allows one to get any line from any file,
caching lines of the file on first access to the file. Although the
file may be any file, the common use is when the file is a Python
script since parsing of the file is done to figure out where the
statement boundaries are when the file is syntax-highlighted. The
syntax-highlighted lines are cached along with the plain text.

The routines here may be is useful when a small random sets of lines
are read from a single file, in particular in a debugger to show
source lines.

A file path can be remapped to another path. This is useful for
example when debugging remotely and the remote file path may be
different from the path on a local filesystem. In the *trepan*
debugger, eval and exec strings are saved in a temporary file and then
the pseudo-filename <string> is remapped to that temporary file name.

Similarly lines within a file can be remapped to other lines. This may
be useful in preprocessors or template systems where ones wants to
make a correspondence between the template file and the expanded
Python file as seen in a tool using that underlying Python file such as
a debugger or profiler.

Summary
-------

.. code:: python

    import pyficache
    lines = pyficache.getlines('/tmp/myprogram.py')
    line = pyficache.getline('/tmp/myprogram.py', 6)
    if len(lines) >= 6:
      assert lines[6] == line

    pyficache.remap_file('/tmp/myprogram.py', 'another-name')
    line_from_alias = pyficache.getline('another-name', 6)
    if len(lines) >= 6:
      assert lines[6] == line_from_alias

    assert '/tmp/myprogram.py', pyficache.remove_remap_file('another-name')
    # another-name is no longer an alias for /tmp/myprogram
    assert None, pyficache.remove_remap_file('another-name')

    pyficache.clear_file_cache()
    pyficache.clear_file_cache('/tmp/myprogram.py')
    pyficache.update_cache()   # Check for modifications of all cached files.

Credits
-------

This is a port of the my Ruby linecache_ module which in turn is based
on the Python linecache module.

coverage_ provides the cool stuff to figure out lines where there
statements.

Other stuff
-----------

Author:   Rocky Bernstein <rockyb@rubyforge.net>
License:  Copyright (c) 2009, 2015 Rocky Bernstein. Released under the GNU GPL 3 license

.. _coverage: http://nedbatchelder.com/code/coverage/
.. _linecache: https://rubygems.org/gems/linecache

.. |Downloads| image:: https://pypip.in/download/pyficache/badge.svg
.. |Build Status| image:: https://travis-ci.org/rocky/python2-trepan.svg
   :target: https://travis-ci.org/rocky/pyficache/
.. |Latest Version| image:: https://pypip.in/version/pyficache/badge.svg?text=version
   :target: https://pypi.python.org/pypi/pyficache/
.. |Supported Python versions| image:: https://pypip.in/py_versions/pyficache/badge.svg
   :target: https://pypi.python.org/pypi/pyficache/
"""
__docformat__ = 'restructuredtext'

from pyficache.main import PYTHON3, PYVER, cache_file, cache_script, cached_files, checkcache, clear_file_cache, clear_file_format_cache, dark_terminal_formatter, file_cache, file2file_remap, getline, getlines, highlight_array, highlight_string, is_cached, is_cached_script, is_mapped_file, light_terminal_formatter, maxline, path, pyc2py, remap_file, remap_file_lines, remove_remap_file, sha1, size, stat, terminal_256_formatter, trace_line_numbers, uncache_script, unmap_file, unmap_file_line, update_cache, update_script_cache # NOQA
