# -*- coding: utf-8 -*-
#   Copyright (C) 2008-2009, 2012-2013, 2015-2016, 2018, 2020
#   Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Read and cache lines of a Python program.

Module to get line from any file, caching lines of the file on
first access to the file. Although the file may be any file, this
package is more tailored to the case where the file is a Python script.

Synopsis
--------

    import pyficache
    filename = __file__ # e.g. '/tmp/myprogram'
     # return all lines of filename as an array
    lines = pyficache.getlines(filename)

     # return line 6, and reload all lines if the file has changed.
    line = pyficache.getline(filename, 6, {'reload_on_change': True})

    # return line 6 syntax highlighted via pygments using style 'emacs'
    line = pyficache.getline(filename, 6, {'style': 'emacs'})

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

import hashlib, linecache, os, re, sys
import os.path as osp

from collections import namedtuple

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter, Terminal256Formatter

from xdis import PYTHON3, PYTHON_VERSION, lineoffsets_in_file
from pyficache.line_numbers import code_linenumbers_in_file

PYVER = "%s%s" % sys.version_info[0:2]

if PYTHON3:
    large_int = sys.maxsize
else:
    large_int = sys.maxint


default_opts = {
    "reload_on_change": False,  # Check if file has changed since last
    # time
    "use_linecache_lines": True,
    "strip_nl": True,  # Strip trailing \n on line returned
    "output": "plain"  # To we want plain output?
    # Set to 'terminal'
    # for terminal syntax-colored output
}


def get_option(key, options):
    global default_opts
    if not options or key not in options:
        return default_opts.get(key)
    else:
        return options[key]
    return None  # Not reached


def has_trailing_nl(string):
    return len(string) > 0 and "\n" == string[-1]


if PYTHON_VERSION >= 3.4:
    from importlib.util import source_from_cache, resolve_name, find_spec
else:
    source_from_cache = resolve_name = find_spec = None


def resolve_name_to_path(path_or_name):
    """Try to "resolve" `path_or_name` info its constituent file path.

    `path_or_name` could be either a

    * a bytecode file path,
    * a module
    * a Python source path already (in which nothing is done)

    We use 3.3, 3.4 importlib routines if these are available.
    If not we'll try other hacky methods.

    If all fails, we'll just return `path_or_name` unchanged.
    """
    if path_or_name.endswith(".py"):
        # Assume Python source code
        return path_or_name

    if source_from_cache:
        try:
            source_path = source_from_cache(path_or_name)
        except:
            pass
        else:
            if source_path:
                return source_path
            pass

    if find_spec:
        try:
            spec = find_spec(path_or_name)
        except:
            spec = None
        else:
            if spec and spec.origin:
                return spec.origin
            pass

    if re.match(".*py[co]$", path_or_name):
        if PYTHON3:
            return re.sub(
                r"(.*)__pycache__/(.+)\.cpython-%s.py[co]$" % PYVER,
                "\\1\\2.py",
                path_or_name,
            )
        else:
            return path_or_name[:-1]

    # If none of the fancy things above happened
    return path_or_name


class LineCacheInfo:
    def __init__(self, stat, line_numbers, linestarts, lines, path, sha1, eols=None):
        self.stat, self.lines, self.path, self.sha1 = (stat, lines, path, sha1)
        self.line_numbers = line_numbers
        self.linestarts = linestarts
        self.eols = eols
        return

    pass


# The file cache. The key is a name as would be given by co_filename
# or __file__. The value is a LineCacheInfo object.
file_cache = {}
script_cache = {}

# `file2file_remap` maps a path (a string) to another path key in file_cache (a
# string).
#
# One important use of file2file_remap is mapping the a full path of a
# file into the name stored in file_cache or given by a Python
# __file__. Applications such as those that get input from users, may
# want to canonicalize the path before looking it up. This map gives a
# way to canonicalize.
#
file2file_remap = {}

# `file2file_remap_lines` goes further than `file2file_remap` and
# allows a path and line number to another path and line number.
#
# One use of this is in translation systems where Python is embedded
# in some other source code. Or perhaps you used uncompyle6 with
# the --linemap option to recreate the source code and want to
# keep the associations between the line numbers in the code
# with line numbers is the recreated source.
#
# The key of `file2file_remap_lines` is the  name of the path as Python
# sees it. For example it would be the name that would be found inside a code
# object co_filename. The value of the dictionary is a RemapLineEntry
# described below

file2file_remap_lines = {}

# `RemapLineEntry` is an entry in file2file_remap_lines with fields:
#
# * `mapped_path` is # the name of the source path.
#    For example this might not be a Python file
#    per se, but the thing from which Python was extracted from.
#
# * `from_to_pairs` is a tuple of integer pairs. For each pair, the first
#    item is a line number in as Python sees it. The second item is the
#    line number in corresponding mapped_path. The the first entry of the
#    pair should always increase from the previous value. The second entry
#    doesn't have to, although in practice it will.

RemapLineEntry = namedtuple("RemapLineEntry", "mapped_path from_to_pairs")

# Example. File "unmapped.template" contains:

#  x = 1; y = 2       # line 1
#  # a comment        # line 2
#  # another comment  # line 3
#  z = 4              # line 4
#  a=5                # line 5

# File "mapped_file.py" contains:

# # This file was recreated from foo.template # line 1
# # and is reformatted according to PEP8 # line 2
# x = 1  # line 3
# y = 2  # line 4
# z = 4  # line 5
# a = 5  # line 6

# file2file_remap_lines = {
#  'foo.template = RemapLineEntry("mapped_file.py", ((1, 3), (4, 5)))
# }

# In this example, line 1 of foo.template corresponds to line 3 of
# mapped_file.py.  There is no line recorded in foo.template that corresponds
# to line 4 of mapped_file. Line 4 of foo.template corresponds to line 5 of
# mapped_file.py. And line 5 of foo.template implicitly corresponds to line 6
# of mapped_file.py since there is nothing to indicate contrary and since that
# line exists in mapped_file.

# Note that this scheme allows the possibility that several co_filenames can be
# mapped to a single file. So a templating system could break a single template
# into several Python files and we can track that. But we not the other way
# around. That is we don't support tracking several templated files which got
# built into a single Python module.

# At such time as the need arises, we will work this.


def clear_file_cache(filename=None):
    """Clear the file cache. If no filename is given clear it entirely.
    if a filename is given, clear just that filename."""
    global file_cache, file2file_remap, file2file_remap_lines
    if filename is not None:
        if filename in file_cache:
            del file_cache[filename]
            pass
    else:
        file_cache = {}
        file2file_remap = {}
        file2file_remap_lines = {}
        pass
    return


def clear_file_format_cache():
    """Remove syntax-formatted lines in the cache. Use this
    when you change the Pygments syntax or Token formatting
    and want to redo how files may have previously been
    syntax marked."""
    for fname, cache_info in file_cache.items():
        for format, lines in cache_info.lines.items():
            if "plain" == format:
                continue
            file_cache[fname].lines[format] = None
            pass
        pass
    pass


def cached_files():
    """Return an array of cached file names"""
    return list(file_cache.keys())


def checkcache(filename=None, opts=False):
    """Discard cache entries that are out of date. If *filename* is *None*
    all entries in the file cache *file_cache* are checked.  If we do not
    have stat information about a file it will be kept. Return a list of
    invalidated filenames.  None is returned if a filename was given but
    not found cached."""

    if isinstance(opts, dict):
        use_linecache_lines = opts["use_linecache_lines"]
    else:
        use_linecache_lines = opts
        pass

    if not filename:
        filenames = list(file_cache.keys())
    elif filename in file_cache:
        filenames = [filename]
    else:
        return None

    result = []
    for filename in filenames:
        if filename not in file_cache:
            continue
        path = file_cache[filename].path
        if osp.exists(path):
            cache_info = file_cache[filename].stat
            stat = os.stat(path)
            if stat and (
                cache_info.st_size != stat.st_size
                or cache_info.st_mtime != stat.st_mtime
            ):
                result.append(filename)
                update_cache(filename, use_linecache_lines)
            else:
                result.append(filename)
                update_cache(filename)
                pass
        pass
    return result


def cache_script(script, text, opts={}):
    """Cache script if it is not already cached."""
    global script_cache
    if script not in script_cache:
        update_script_cache(script, text, opts)
        pass
    return script


def uncache_script(script, opts={}):
    """remove script from cache."""
    global script_cache
    if script in script_cache:
        del script_cache[script]
        return script
    return None


def update_script_cache(script, text, opts={}):
    """Cache script if it is not already cached."""
    global script_cache
    if script not in script_cache:
        script_cache[script] = text
    return script


def cache_file(filename, reload_on_change=False, opts=default_opts):
    """Cache filename if it is not already cached.
    Return the expanded filename for it in the cache
    or nil if we can not find the file."""
    filename = resolve_name_to_path(filename)
    if filename in file_cache:
        if reload_on_change:
            checkcache(filename)
        pass
    else:
        opts["use_linecache_lines"] = True
        update_cache(filename, opts)
        pass
    if filename in file_cache:
        return file_cache[filename].path
    else:
        return None
    return  # Not reached


def is_cached(file_or_script):
    """Return True if file_or_script is cached"""
    if isinstance(file_or_script, str):
        return unmap_file(file_or_script) in file_cache
    else:
        return is_cached_script(file_or_script)
    return


def is_cached_script(filename):
    return unmap_file(filename) in list(script_cache.keys())


def is_empty(filename):
    filename = unmap_file(filename)
    return 0 == len(file_cache[filename].lines["plain"])


def getline(file_or_script, line_number, opts=default_opts):
    """Get line *line_number* from file named *file_or_script*. Return None if
    there was a problem or it is not found.

    Example:

    lines = pyficache.getline("/tmp/myfile.py")
    """
    filename = unmap_file(file_or_script)
    filename, line_number = unmap_file_line(filename, line_number)
    lines = getlines(filename, opts)
    if lines and line_number >= 1 and line_number <= maxline(filename):
        line = lines[line_number - 1]
        if get_option("strip_nl", opts):
            return line.rstrip("\n")
        else:
            return line
        pass
    else:
        return None
    return  # Not reached


def getlines(filename, opts=default_opts):
    """Read lines of *filename* and cache the results. However, if
    *filename* was previously cached use the results from the
    cache. Return *None* if we can not get lines
    """
    if get_option("reload_on_change", opts):
        checkcache(filename)
    fmt = get_option("output", opts)
    highlight_opts = {"bg": fmt}
    cs = opts.get("style")

    # Colorstyle of Terminal255Formatter takes precidence over
    # light/dark colorthemes of TerminalFormatter
    if cs:
        highlight_opts["style"] = cs
        fmt = cs

    if filename not in file_cache:
        update_cache(filename, opts)
        filename = resolve_name_to_path(filename)
        if filename not in file_cache:
            return None
        pass
    lines = file_cache[filename].lines
    if fmt not in lines.keys():
        lines[fmt] = highlight_array(lines["plain"], **highlight_opts)
        pass
    return lines[fmt]


def highlight_array(array, trailing_nl=True, bg="light", **options):
    fmt_array = highlight_string("".join(array), bg, **options).split("\n")
    lines = [line + "\n" for line in fmt_array]
    if not trailing_nl:
        lines[-1] = lines[-1].rstrip("\n")
    return lines


python_lexer = PythonLexer()

# TerminalFormatter uses a colorTHEME with light and dark pairs.
# But Terminal256Formatter uses a colorSTYLE.  Ugh
dark_terminal_formatter = TerminalFormatter(bg="dark")
light_terminal_formatter = TerminalFormatter(bg="light")
terminal_256_formatter = Terminal256Formatter()


def highlight_string(string, bg="light", **options):
    global terminal_256_formatter
    if options.get("style"):
        if terminal_256_formatter.style != options["style"]:
            terminal_256_formatter = Terminal256Formatter(style=options["style"])
            del options["style"]
        return highlight(string, python_lexer, terminal_256_formatter, **options)
    elif "light" == bg:
        return highlight(string, python_lexer, light_terminal_formatter, **options)
    else:
        return highlight(string, python_lexer, dark_terminal_formatter, **options)
    pass


def path(filename):
    """Return full filename path for filename"""
    filename = unmap_file(filename)
    if filename not in file_cache:
        return None
    return file_cache[filename].path


def remap_file(from_file, to_file):
    """Make *to_file* be a synonym for *from_file*"""
    file2file_remap[to_file] = from_file
    return


def remap_file_lines(from_path, to_path, line_map_list):
    """Adds line_map list to the list of association of from_file to
       to to_file"""
    from_path = resolve_name_to_path(from_path)
    cache_file(to_path)
    remap_entry = file2file_remap_lines.get(to_path)
    if remap_entry:
        new_list = list(remap_entry.from_to_pairs) + list(line_map_list)
    else:
        new_list = line_map_list
    # FIXME: look for duplicates ?
    file2file_remap_lines[to_path] = RemapLineEntry(
        from_path, tuple(sorted(new_list, key=lambda t: t[0]))
    )
    return


def remove_remap_file(filename):
    """Remove any mapping for *filename* and return that if it exists"""
    global file2file_remap
    if filename in file2file_remap:
        retval = file2file_remap[filename]
        del file2file_remap[filename]
        return retval
    return None


def sha1(filename):
    """Return SHA1 of filename."""
    filename = unmap_file(filename)
    if filename not in file_cache:
        cache_file(filename)
        if filename not in file_cache:
            return None
        pass
    if file_cache[filename].sha1:
        return file_cache[filename].sha1.hexdigest()
    sha1 = hashlib.sha1()
    for line in file_cache[filename].lines["plain"]:
        sha1.update(line.encode("utf-8"))
        pass
    file_cache[filename].sha1 = sha1
    return sha1.hexdigest()


def size(filename, use_cache_only=False):
    """Return the number of lines in filename. If `use_cache_only' is False,
    we'll try to fetch the file if it is not cached."""
    filename = unmap_file(filename)
    if filename not in file_cache:
        if not use_cache_only:
            cache_file(filename)
        if filename not in file_cache:
            return None
        pass
    return len(file_cache[filename].lines["plain"])


def maxline(filename, use_cache_only=False):
    """Return the maximum line number filename after taking into account
    line remapping. If no remapping then this is the same as size"""
    if filename not in file2file_remap_lines:
        return size(filename, use_cache_only)
    max_lineno = -1
    remap_line_entry = file2file_remap_lines.get(filename)
    if not remap_line_entry:
        return size(filename, use_cache_only)
    for t in remap_line_entry.from_to_pairs:
        max_lineno = max(max_lineno, t[1])
    if max_lineno == -1:
        return size(filename, use_cache_only)
    else:
        return max_lineno


def stat(filename, use_cache_only=False):
    """Return stat() info for *filename*. If *use_cache_only* is *False*,
    we will try to fetch the file if it is not cached."""
    filename = resolve_name_to_path(filename)
    if filename not in file_cache:
        if not use_cache_only:
            cache_file(filename)
        if filename not in file_cache:
            return None
        pass
    return file_cache[filename].stat


def trace_line_numbers(filename, reload_on_change=False, toplevel_only=False):
    """Return the line numbers that are (or would be) stored in
    co_linenotab for `filename`.

    These are places setting a breakpoint could conceivably
    trigger. On other lines, a breakpoint would never occur, because
    only the Python interpreter only stops at bytecode offsets
    that have a line number.

    The line in the source file could be empty because the line is
    blank, inside a string or comment, in the middle of some long
    construct or is something of that ilk.
    """
    fullname = cache_file(filename, reload_on_change)
    if not fullname:
        return None
    e = file_cache[filename]
    if not e.line_numbers:
        e.line_numbers = code_linenumbers_in_file(fullname)
        pass
    return e.line_numbers


def cache_code_lines(
    filename, reload_on_change=False, toplevel_only=False, include_offsets=True
):
    """Cache line numbers, bytecode offsets, and code object that are
    (or would be) stored in the bytecode for `filename`.

    These are places setting a breakpoint could conceivably
    trigger. On other lines, a breakpoint would never occur, because
    only the Python interpreter only stops at bytecode offsets
    that have a line number.

    The line in the source file could be empty because the line is
    blank, inside a string or comment, in the middle of some long
    construct or is something of that ilk.

    Internally the co_lineno table in the code to get this. But here,
    you don't need to know that. xdis does the heavy lifting.
    """
    fullname = cache_file(filename, reload_on_change)
    if not fullname:
        return None
    file_info = file_cache[filename]
    if not file_info.line_numbers:
        code_info = lineoffsets_in_file(fullname, toplevel_only=toplevel_only)
        file_info.line_numbers = code_info.line_numbers(include_offsets=include_offsets)
        file_info.linestarts = code_info.linestarts
        pass
    return file_info


def code_lines(
    filename, reload_on_change=False, toplevel_only=False, include_offsets=True
):
    """Return the line numbers, bytecode offsets, and code object that are
    (or would be) stored in the bytecode for `filename`.
    """
    file_info = cache_code_lines(filename, toplevel_only, include_offsets)
    if not file_info:
        return None
    return file_info


def code_line_info(
    filename,
    line_number,
    reload_on_change=False,
    toplevel_only=False,
    include_offsets=True,
):
    """Return the bytecode information that is associated with
    `line_number` in the bytecode for `filename`.
    """
    file_info = cache_code_lines(filename,
                                 reload_on_change=reload_on_change,
                                 toplevel_only=toplevel_only,
                                 include_offsets=include_offsets)
    if not file_info:
        return None
    return file_info.line_numbers.get(line_number, None)


def code_offset_info(
    filename, offset, reload_on_change=False,
):
    """Return the bytecode information that is associated with
    `offset` in the bytecode for `filename`.

    Each entry is a line number list of instruction offests associated
    with that line number and a code object where this can be found.

    This comes from findlinestarts() from xdis which is the same
    as findlinestarts() in xdis.
    """

    # THINK ABOUT:
    # We set toplevel_only to False, because we cache
    # information and want to cache information about the entire file,
    # even though we accept offsets for only toplevel.
    # Perhaps we should revise the API
    file_info = code_lines(filename, toplevel_only=False, include_offsets=True)

    return file_info.linestarts.get(offset, None)


def is_mapped_file(filename):
    if filename in file2file_remap:
        return "file"
    elif file2file_remap_lines.get(filename):
        return "file_line"
    else:
        return None


def unmap_file(filename):
    # FIXME: this is wrong?
    return file2file_remap.get(filename, filename)


def unmap_file_line(filename, line_number, reverse=False):
    remap_line_entry = file2file_remap_lines.get(filename)
    mapped_line_number = line_number
    if remap_line_entry:
        filename = remap_line_entry.mapped_path
        cache_entry = file_cache.get(filename, None)
        if cache_entry:
            line_max = maxline(filename)
        else:
            line_max = large_int
        last_t = (1, 1)
        # FIXME: use binary search
        # Note we assume assume from_line is increasing.
        # Add sentinel at end of from pairs to handle using the final
        # entry for line numbers greater than it.
        # Find the closest mapped line number equal or before line_number.
        for t in remap_line_entry.from_to_pairs + ((large_int, line_max),):
            if reverse:
                t = list(reversed(t))
            if t[1] == line_number:
                mapped_line_number = t[0]
                break
            elif t[1] > line_number:
                mapped_line_number = last_t[0] + (line_number - last_t[1])
                break
            last_t = t
        pass
    return (filename, mapped_line_number)


def update_cache(filename, opts=default_opts, module_globals=None):
    """Update a cache entry.  If something is wrong, return
    *None*. Return *True* if the cache was updated and *False* if not.  If
    *use_linecache_lines* is *True*, use an existing cache entry as source
    for the lines of the file."""

    if not filename:
        return None

    orig_filename = filename
    filename = resolve_name_to_path(filename)
    if filename in file_cache:
        del file_cache[filename]
    path = osp.abspath(filename)
    stat = None
    if get_option("use_linecache_lines", opts):
        fname_list = [filename]
        mapped_path = file2file_remap.get(path)
        if mapped_path:
            fname_list.append(mapped_path)
            for filename in fname_list:
                try:
                    stat = os.stat(filename)
                    plain_lines = linecache.getlines(filename)
                    trailing_nl = has_trailing_nl(plain_lines[-1])
                    lines = {
                        "plain": plain_lines,
                    }
                    file_cache[filename] = LineCacheInfo(
                        stat=stat,
                        line_numbers=None,
                        linestarts=None,
                        lines=lines,
                        path=path,
                        sha1=None,
                    )
                except:
                    pass
                pass
            if orig_filename != filename:
                file2file_remap[orig_filename] = filename
                file2file_remap[osp.abspath(orig_filename)] = filename
                pass
            file2file_remap[path] = filename
            return filename
        pass
    pass

    if osp.exists(path):
        stat = os.stat(path)
    elif module_globals and "__loader__" in module_globals:
        name = module_globals.get("__name__")
        loader = module_globals["__loader__"]
        get_source = getattr(loader, "get_source", None)
        if name and get_source:
            try:
                data = get_source(name)
            except (ImportError, IOError):
                pass
            else:
                if data is None:
                    # No luck, the PEP302 loader cannot find the source
                    # for this module.
                    return None
                # FIXME: DRY with code below
                lines = {"plain": data.splitlines()}
                raw_string = "".join(lines["plain"])
                trailing_nl = has_trailing_nl(raw_string)
                if "style" in opts:
                    key = opts["style"]
                    highlight_opts = {"style": key}
                else:
                    key = "terminal"
                    highlight_opts = {}

                lines[key] = highlight_array(
                    raw_string.split("\n"), trailing_nl, **highlight_opts
                )
                file_cache[filename] = LineCacheInfo(
                    stat=None, lines=lines, linestarts=None, path=filename, sha1=None
                )
                file2file_remap[path] = filename
                return True
            pass
        pass
    if not osp.isabs(filename):
        # Try looking through the module search path, which is only useful
        # when handling a relative filename.
        stat = None
        for dirname in sys.path:
            path = osp.join(dirname, filename)
            if osp.exists(path):
                stat = os.stat(path)
                break
            pass
        if not stat:
            return False
        pass

    try:
        mode = "r" if PYTHON3 else "rU"
        with open(path, mode) as fp:
            lines = {"plain": fp.readlines()}
            eols = fp.newlines
    except:
        return None

    # FIXME: DRY with code above
    raw_string = "".join(lines["plain"])
    trailing_nl = has_trailing_nl(raw_string)
    if "style" in opts:
        key = opts["style"] or "default"
        highlight_opts = {"style": key}
    else:
        key = "terminal"
        highlight_opts = {}

    lines[key] = highlight_array(raw_string.split("\n"), trailing_nl, **highlight_opts)
    if orig_filename != filename:
        file2file_remap[orig_filename] = filename
        file2file_remap[osp.abspath(orig_filename)] = filename
        pass
    pass

    file_cache[filename] = LineCacheInfo(
        stat=stat,
        line_numbers=None,
        linestarts=None,
        lines=lines,
        path=path,
        sha1=None,
        eols=eols,
    )
    file2file_remap[path] = filename
    return True


# example usage
if __name__ == "__main__":

    z = lambda x, y: x + y

    def yes_no(var):
        # NOTE: for testing, we want the next line to contain 2 statements on a
        # single line
        prefix1 = ""
        prefix2 = "not "
        if var:
            return prefix1
        else:
            return prefix2
        return  # Not reached

    # print(resolve_name_to_path("os"))
    # print(getline(__file__, 1, {"output": "dark"}))
    # print(getline(__file__, 2, {"output": "light"}))
    # from pygments.styles import STYLE_MAP

    # opts = {"style": list(STYLE_MAP.keys())[0]}
    # print(getline(__file__, 1, opts))
    # update_cache("os")

    # lines = getlines(__file__)
    # print("%s has %s lines" % (__file__, len(lines)))
    # lines = getlines(__file__, {"output": "light"})

    # i = 0
    # for line in lines:
    #     i += 1
    #     print(line.rstrip("\n").rstrip("\n"))
    #     if i > 20:
    #         break
    #     pass
    # line = getline(__file__, 6)
    # print("The 6th line is\n%s" % line)
    # line = remap_file(__file__, "another_name")
    # print(getline("another_name", 7))

    # print("Files cached: %s" % cached_files())

    update_cache(__file__)
    checkcache(__file__)
    print("%s has %s lines" % (__file__, size(__file__)))
    print("%s code_lines data:\n" % __file__)

    line_info = code_offset_info(__file__, 0)
    print("Starting line for file (bytecode offset 0) is %s" % line_info)
    line_info = code_lines(__file__).line_numbers
    for line_num, li in line_info.items():
        print("\tline: %4d: %s" % (line_num, ", ".join([str(i.offsets) for i in li])))
    print("=" * 30)

    # print("%s is %scached." % (__file__, yes_no(is_cached(__file__))))
    # print(stat(__file__))
    # print("Full path: %s" % path(__file__))
    # checkcache()  # Check all files in the cache
    # clear_file_format_cache()
    # clear_file_cache()
    # print(("%s is now %scached." % (__file__, yes_no(is_cached(__file__)))))
    # #   # digest = SCRIPT_LINES__.select{|k,v| k =~ /digest.rb$/}
    # #   # if digest is not None: print digest.first[0]
    # line = getline(__file__, 7)
    # print("The 7th line is\n%s" % line)
    # orig_path = __file__
    # mapped_path = "test2"
    # start_line = 10
    # start_mapped = 6
    # remap_file_lines(orig_path, mapped_path, ((start_line, start_mapped),))
    # for l in (1,):
    #     line = getline(mapped_path, l + start_mapped)
    # print(
    #     "Remapped %s line %d should be line %d of %s. line is:\n%s"
    #     % (mapped_path, start_mapped + l, start_line + l, orig_path, line)
    # )
    # print("XXX", file2file_remap_lines)
