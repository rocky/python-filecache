"""
  Copyright (c) 2018 by Rocky Bernstein
"""
__docformat__ = 'restructuredtext'

# Export some functions
from pyficache.main import (
    PYTHON3,
    PYVER,
    cache_file,
    cache_script,
    cached_files,
    checkcache,
    clear_file_cache,
    clear_file_format_cache,
    dark_terminal_formatter,
    file_cache,
    file2file_remap,
    getline,
    getlines,
    highlight_array,
    highlight_string,
    is_cached,
    is_cached_script,
    is_mapped_file,
    light_terminal_formatter,
    maxline,
    path,
    pyc2py,
    remap_file,
    remap_file_lines,
    remove_remap_file,
    sha1,
    size,
    stat,
    terminal_256_formatter,
    trace_line_numbers,
    uncache_script,
    unmap_file,
    unmap_file_line,
    update_cache,
    update_script_cache,
)