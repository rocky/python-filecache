# -*- coding: utf-8 -*-
#  Copyright (C) 2015, 2018, 2020, 2023-2024 Rocky Bernstein <rocky@gnu.org>
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
Synopsis
--------

The *pyficache* module allows one to get any line from any file,
caching lines of the file on first access to the file. Although the
file may be any file, this package is more tailored to the case
where the file is a Python script.

Here, the file is parsed to determine statement bounderies,
and a copies of the file syntax-highlighted are also saved.

Also saved is file information such as when the file was last modified
and a SHA1 of the file. These are useful in determining if the file
has changed and verifying the contents of the file.

By caching contents, access is sped up when small small random sets of lines
are read from a single file, in particular in a debugger to show
source lines.

A file path can be remapped to another path. This is useful for
example when debugging remotely and the remote file path may be
different from the path on a local filesystem. In the `trepan3 <https://pypi.python.org/pypi/trepan3k>`_
and `trepan2 <https://pypi.python.org/pypi/trepan2>`_ debuggers, *eval* and *exec* strings are
saved in a temporary file and then the pseudo-filename `<string>` is
remapped to that temporary file name.

Similarly lines within a file can be remapped to other lines. This may
be useful in preprocessors or template systems where ones wants to
make a correspondence between the template file and the expanded
Python file as seen in a tool using that underlying Python file such as
a debugger or profiler.

Summary
-------

.. code:: python

    import pyficache
    filename = __file__ # e.g. '/tmp/myprogram'
     # return all lines of filename as an array
    lines = pyficache.getlines(filename)

     # return line 6, and reload all lines if the file has changed.
    line = pyficache.getline(filename, 6, {'reload_on_change': True})

    # return line 6 syntax highlighted via pygments using style 'colorful'
    line = pyficache.getline(filename, 6, {'style': 'colorful'})

    pyficache.remap_file('/tmp/myprogram.py', 'another-name')
    line_from_alias = pyficache.getline('another-name', 6)

    assert __file__, pyficache.remove_remap_file('another-name')

    # another-name is no longer an alias for /tmp/myprogram
    assert None, pyficache.remove_remap_file('another-name')

    # Clear cache for __file__
     pyficache.clear_file_cache(__file__)

    # Clear all cached files.
    pyficache.clear_file_cache()

    # Check for modifications of all cached files.
    pyficache.update_cache()
"""

__docformat__ = "restructuredtext"

# Export some functions
from pyficache.main import (
    PYVER,
    add_remap_pat,
    cache_code_lines,
    cache_file,
    cache_script,
    cached_files,
    checkcache,
    clear_file_cache,
    clear_file_format_cache,
    code_line_info,
    code_lines,
    code_offset_info,
    # dark_terminal_formatter,
    file_cache,
    file2file_remap,
    getline,
    getlines,
    highlight_array,
    highlight_string,
    is_cached,
    is_cached_script,
    is_mapped_file,
    # light_terminal_formatter,
    maxline,
    path,
    remap_file,
    remap_file_lines,
    remap_file_pat,
    remove_remap_file,
    resolve_name_to_path,
    sha1,
    size,
    stat,
    # terminal_256_formatter,
    trace_line_numbers,
    uncache_script,
    unmap_file,
    unmap_file_line,
    update_cache,
    update_script_cache,
)
from pyficache.version import __version__

__all__ = [
    "__version__",
    "PYVER",
    "add_remap_pat",
    "cache_code_lines",
    "cache_file",
    "cache_script",
    "cached_files",
    "checkcache",
    "clear_file_cache",
    "clear_file_format_cache",
    "code_line_info",
    "code_lines",
    "code_offset_info",
    "dark_terminal_formatter",
    "file_cache",
    "file2file_remap",
    "getline",
    "getlines",
    "highlight_array",
    "highlight_string",
    "is_cached",
    "is_cached_script",
    "is_mapped_file",
    "light_terminal_formatter",
    "maxline",
    "path",
    "remap_file",
    "remap_file_lines",
    "remap_file_pat",
    "remove_remap_file",
    "resolve_name_to_path",
    "sha1",
    "size",
    "stat",
    "terminal_256_formatter",
    "trace_line_numbers",
    "uncache_script",
    "unmap_file",
    "unmap_file_line",
    "update_cache",
    "update_script_cache",
]
