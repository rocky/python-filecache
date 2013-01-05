# -*- coding: utf-8 -*-
#   Copyright (C) 2008-2009, 2012-2013 Rocky Bernstein <rocky@gnu.org>
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
'''A module to read and cache lines of a Python program.'''

import coverage, hashlib, linecache, os, sys, types

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

default_opts = {
    'reload_on_change'    : False,  # Check if file has changed since last time
    'use_linecache_lines' : True,  
    'strip_nl'            : True,   # Strip trailing \n on line returned
    'output'              : 'plain' # To we want plain output? Set to 'terminal'
                                    # for terminal syntax-colored output
    }

def get_option(key, options):
    global default_opts
    if not options or key not in options:
        return default_opts.get(key)
    else:
        return options[key]
    return None # Not reached

def has_trailing_nl(string):
    return '\n' == string[-1]

def pyc2py(filename):
    if '.pyc' == filename[-4:]:
        return filename[:-1]
    return filename

class LineCacheInfo:
    def __init__(self, stat, line_numbers, lines, path, sha1):
        self.stat, self.lines, self.path, self.sha1 = (stat, lines, path, sha1)
        self.line_numbers = line_numbers
        return
    pass

# The file cache. The key is a name as would be given by co_filename
# or __file__. The value is a LineCacheInfo object. 
file_cache = {}
script_cache = {}

# Maps a string filename (a String) to a key in file_cache (a String).
#
# One important use of file2file_remap is mapping the a full path of a
# file into the name stored in file_cache or given by a Python
# __file__. Applications such as those that get input from users, may
# want canonicalize a file name before looking it up. This map gives a
# way to do that.
#
# Another related use is when a template system is used.  Here we'll
# probably want to remap not only the file name but also line
# ranges. Will probably use this for that, but I'm not sure.
file2file_remap = {} 
file2file_remap_lines = {}
  
# Clear the file cache. If no filename is given clear it entirely.
# if a filename is given, clear just that filename.
def clear_file_cache(filename=None):
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
    '''Remove syntax-formatted lines in the cache. Use this
    when you change the Pygments syntax or Token formatting
    and want to redo how files may have previously been 
    syntax marked.'''
    for fname, cache_info in file_cache.iteritems():
        for fmt in cache_info.lines:
            if 'plain' == fmt: continue
            file_cache[fname].lines[fmt] = None
            pass
        pass
    pass

def clear_script_cache():
    '''Clear the script cache entirely.'''
    script_cache = {}
    pass

def cached_files():
    '''Return an array of cached file names'''
    return file_cache.keys()

def checkcache(filename=None, opts=False):
    '''Discard cache entries that are out of date. If *filename* is *None*
    all entries in the file cache *file_cache* are checked.  If we do not
    have stat information about a file it will be kept. Return a list of
    invalidated filenames.  None is returned if a filename was given but
    not found cached.'''
    
    if isinstance(opts, types.DictType):
        use_linecache_lines = opts['use_linecache_lines']
    else:
        use_linecache_lines = opts
        pass

    if not filename:
      filenames = file_cache.keys()
    elif filename in file_cache:
      filenames = [filename]
    else:
      return None
    
    result = []
    for filename in filenames:
        if filename not in file_cache: continue
        path = file_cache[filename].path
        if os.path.exists(path):
            cache_info = file_cache[filename].stat
            stat = os.stat(path)
            if stat and \
                    (cache_info.st_size != stat.st_size or \
                         cache_info.st_mtime != stat.st_mtime):
                result.append(filename)
                update_cache(filename, use_linecache_lines)
            else:
                result.append(filename)
                update_cache(filename)
                pass
        pass
    return result

def cache_script(script, opts={}):
    '''Cache script if it is not already cached.'''
    global script_cache
    if script in script_cache:
        update_script_cache(script, opts)
        pass
    return script

def cache_file(filename, reload_on_change=False, opts=default_opts):
    '''Cache filename if it is not already cached.
    Return the expanded filename for it in the cache
    or nil if we can not find the file.'''
    global file_cache
    filename = pyc2py(filename)
    if filename in file_cache:
        if reload_on_change: checkcache(filename)
        pass
    else:
        opts['use_linecache_lines'] = True
        update_cache(filename, opts)
        pass
    if filename in file_cache:
      return file_cache[filename].path
    else: return None
    return # Not reached

def cache(filename, reload_on_change=False):
    '''Older routine - for compability.  Cache filename if it is not
    already cached.  Return the expanded filename for it in the cache
    or None if we ca not find the file.'''
    global file_cache
    if filename in file_cache:
        if reload_on_change: checkcache(filename)
        pass
    else:
        update_cache(filename, {'reload_on_change': True})
        pass
    orig_filename = filename
    filename = pyc2py(filename)
    if filename in file_cache:
        if orig_filename != filename:
            remap_file(orig_filename, file_cache[filename].path)
            pass
        return file_cache[filename].path
    else:
        return None
    pass

def is_cached(file_or_script):
    '''Return True if file_or_script is cached'''
    global file_cache
    if isinstance(file_or_script, types.StringType):
        return unmap_file(file_or_script) in file_cache
    else:
        return is_cached_script(file_or_script)
    return

def is_cached_script(filename):
    global script_cache
    return unmap_file(filename) in keys(script_cache)

def is_empty(filename):
    filename=unmap_file(filename)
    return 0 == len(file_cache[filename].lines['plain'])

def getline(file_or_script, line_number, opts=default_opts):
    '''Get line *line_number* from file named *file_or_script*. Return None if
    there was a problem or it is not found.

    Example:

    lines = pyficache.getline("/tmp/myfile.py")
    '''
    # Compatibility with older interface
    if not isinstance(opts, types.DictType):
        global default_opts
        r_o_c = opts
        opts = default_opts
        opts['reload_on_change'] = r_o_c
        pass
    filename = unmap_file(file_or_script)
    filename, line_number = unmap_file_line(filename, line_number)
    lines = getlines(filename, opts)
    if lines and line_number >=1 and line_number <= len(lines):
        line = lines[line_number-1]
        if get_option('strip_nl', opts):
            return line.rstrip('\n')
        else:
            return line
        pass
    else:
        return None
    return # Not reached

def getlines(filename, opts=default_opts):
    '''Read lines of <filename> and cache the results. However, if
    <filename> was previously cached use the results from the
    cache. Return None if we can not get lines
    '''
    global file_cache
    if get_option('reload_on_change', opts): checkcache(filename)
    fmt = get_option('output', opts)
    if filename not in file_cache:
        update_cache(filename, opts)
        filename = pyc2py(filename)
        if filename not in file_cache: return None
        pass
    lines = file_cache[filename].lines
    if fmt not in lines:
        lines[fmt] = highlight_array(lines['plain'], light_or_dark=fmt)
        pass
    return lines[fmt]

def highlight_array(array, trailing_nl=True,
                    light_or_dark='light'):
    fmt_array = highlight_string(''.join(array),
                                 light_or_dark).split('\n')
    lines = [ line + "\n" for line in fmt_array ]
    if not trailing_nl: lines[-1] = lines[-1].rstrip('\n')
    return lines

python_lexer = PythonLexer()
dark_terminal_formatter=TerminalFormatter(bg = 'dark')
light_terminal_formatter=TerminalFormatter(bg = 'light')

def highlight_string(string, light_or_dark='light'):
    global python_lexer
    if 'light' == light_or_dark:
        global light_terminal_formatter
        return highlight(string, python_lexer, light_terminal_formatter)
    else:
        global darkterminal_formatter
        return highlight(string, python_lexer, dark_terminal_formatter)
    pass

def path(filename):
    '''Return full filename path for filename'''
    filename = unmap_file(filename)
    if filename not in file_cache:
        return None
    return file_cache[filename].path

def remap_file(from_file, to_file):
    file2file_remap[to_file] = from_file
    return

def remap_file_lines(from_file, to_file, line_range, start):
    from_file = pyc2py(from_file)
    if isinstance(line_range, types.IntType):
        line_range = range(line_range, line_range+1)
        pass
    if to_file is None: to_file = from_file 
    if file2file_remap_lines.get(to_file):
        # FIXME: need to check for overwriting ranges: whether
        # they intersect or one encompasses another.
        file2file_remap_lines[to_file].append([from_file, line_range, start])
    else:
        file2file_remap_lines[to_file] = [[from_file, line_range, start]]
        pass
    return

def sha1(filename):
    '''Return SHA1 of filename.'''
    filename = unmap_file(filename)
    if filename not in file_cache: 
        cache(filename)
        if filename not in file_cache: 
            return None
        pass
    if file_cache[filename].sha1:
        return file_cache[filename].sha1.hexdigest()
    sha1 = hashlib.sha1()
    for line in file_cache[filename].lines['plain']:
        sha1.update(line)
        pass
    file_cache[filename].sha1 = sha1
    return sha1.hexdigest()
      
def size(filename, use_cache_only=False):
    '''Return the number of lines in filename. If `use_cache_only' is False,
    we'll try to fetch the file if it is not cached.'''
    filename = unmap_file(filename)
    if filename not in file_cache: 
        if not use_cache_only: cache(filename)
        if filename not in file_cache: 
            return None
        pass
    return len(file_cache[filename].lines['plain'])

def stat(filename, use_cache_only=False):
    '''Return stat() info for *filename*. If *use_cache_only* is False,
    we will try to fetch the file if it is not cached.'''
    filename = pyc2py(filename)
    if filename not in file_cache: 
        if not use_cache_only: cache(filename)
        if filename not in file_cache: 
            return None
        pass
    return file_cache[filename].stat

def trace_line_numbers(filename, reload_on_change=False):
    '''Return an Array of breakpoints in filename.
    The list will contain an entry for each distinct line event call
    so it is possible (and possibly useful) for a line number appear more
    than once.'''
    fullname = cache(filename, reload_on_change)
    if not fullname: return None
    e = file_cache[filename]
    if not e.line_numbers:
        if hasattr(coverage.coverage, 'analyze_morf'):
            e.line_numbers = coverage.the_coverage.analyze_morf(fullname)[1]
        else:
            cov = coverage.coverage()
            cov._warn_no_data = False
            e.line_numbers = cov.analysis(fullname)[1]
            pass
        pass
    return e.line_numbers

def unmap_file(filename):
    if filename in file2file_remap : return file2file_remap[filename] 
    else: return filename
    return # Not reached
    
def unmap_file_line(filename, line):
    if file2file_remap_lines.get(filename):
        for from_file, line_range, start in file2file_remap_lines[filename]:
            if line_range == line:
                from_file = from_file or filename
                pass
            return [from_file, start+line-line_range[0]] 
        pass
    return [filename, line]

def update_cache(filename, opts=default_opts):
    '''Update a cache entry.  If something is wrong, return
    None. Return True if the cache was updated and False if not.  If
    use_linecache_lines is True, use an existing cache entry as source
    for the lines of the file.'''
    
    if not filename: return None

    orig_filename = filename
    filename = pyc2py(filename)
    if filename in file_cache: del file_cache[filename]
    path = os.path.abspath(filename)
    
    if get_option('use_linecache_lines', opts):
      fname_list = [filename]
      if file2file_remap.get(path):
          fname_list.append(file2file_remap[path]) 
          for filename in fname_list:
              try:
                  stat = os.stat(filename)
                  plain_lines = linecache.getlines(filename)
                  trailing_nl = has_trailing_nl(plain_lines[-1])
                  lines = {
                      'plain'   : plain_lines,
                      }
                  file_cache[filename] = LineCacheInfo(stat, None, lines, path, 
                                                       None)
              except:
                  stat = None
                  pass
              pass
          if orig_filename != filename:
              file2file_remap[orig_filename] = filename
              file2file_remap[os.path.abspath(orig_filename)] = filename
              pass
          file2file_remap[path] = filename
          return filename
      pass
    pass
      
    if os.path.exists(path):
        stat = os.stat(path)
    elif os.path.basename(filename) == filename:
        # try looking through the search path.
        stat = None
        for dirname in sys.path:
            path = os.path.join(dirname, filename)
            if os.path.exists(path):
                stat = os.stat(path)
                break
            pass
        if not stat: return False 
        pass
    try:
        fp = open(path, 'r')
        lines = {'plain' : fp.readlines()}
        fp.close()
        raw_string        = ''.join(lines['plain'])
        trailing_nl       = has_trailing_nl(raw_string)
        lines['terminal'] = highlight_array(raw_string.split('\n'),
                                            trailing_nl)
        if orig_filename != filename:
            file2file_remap[orig_filename] = filename
            file2file_remap[os.path.abspath(orig_filename)] = filename
            pass
        pass
    
    except:
        ##  print '*** cannot open', path, ':', msg
        return None
    
    file_cache[filename] = LineCacheInfo(os.stat(path), None, lines,
                                         path, None)
    file2file_remap[path] = filename
    return True

# example usage
if __name__ == '__main__':
  def yes_no(var):
    if var: return "" 
    else: return "not "
    return # Not reached

  print getline(__file__, 1, {'output': 'dark'})
  update_cache('os')

  lines = getlines(__file__)
  print "%s has %s lines" % (__file__, len(lines))
  lines = getlines(__file__, {'output': 'light'})
  i = 0
  for line in lines:
      i += 1
      print line.rstrip('\n').rstrip('\n')
      if i > 20: break
      pass
  line = getline(__file__, 6)
  print "The 6th line is\n%s" % line
  line = remap_file(__file__, 'another_name')
  print getline('another_name', 7)

  print "Files cached: %s" % cached_files()
  update_cache(__file__)
  checkcache(__file__)
  print "%s has %s lines" % (__file__, size(__file__))
  print "%s trace line numbers:\n" % __file__
  print "%s " % repr(trace_line_numbers(__file__))
  print "%s is %scached." % (__file__, 
                             yes_no(is_cached(__file__)))
  print stat(__file__)
  print "Full path: %s" % path(__file__)
  checkcache() # Check all files in the cache
  clear_file_format_cache()
  clear_file_cache()
  print("%s is now %scached." % (__file__, yes_no(is_cached(__file__))))
  #   # digest = SCRIPT_LINES__.select{|k,v| k =~ /digest.rb$/}
  #   # if digest is not None: print digest.first[0]
  line = getline(__file__, 7)
  print "The 7th line is\n%s" % line
  remap_file_lines(__file__, 'test2', range(10,21), 6)
  line = getline('test2', 11)
  print "Remapped 11th line of test2 is:\n%s" % line
