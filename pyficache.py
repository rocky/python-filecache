# -*- coding: utf-8 -*-
#   Copyright (C) 2008, 2009 Rocky Bernstein <rocky@gnu.org>
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

class LineCacheInfo:
    def __init__(self, stat, line_numbers, lines, path, sha1):
        self.stat, self.lines, self.path, self.sha1 = (stat, lines, path, sha1)
        self.line_numbers = line_numbers
        return
    pass

# The file cache. The key is a name as would be given by co_filename
# or __file__. The value is a LineCacheInfo object. 
file_cache = {}

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
  
# Clear the file cache entirely.
def clear_file_cache():
    global file_cache, file2file_remap, file2file_remap_lines
    file_cache = {}
    file2file_remap = {}
    file2file_remap_lines = {}
    return

# Return an array of cached file names
def cached_files():
    return file_cache.keys()

# Discard cache entries that are out of date. If +filename+ is +None+
# all entries in the file cache +file_cache+ are checked.  If we don't
# have stat information about a file it will be kept. Return a list of
# invalidated filenames.  None is returned if a filename was given but
# not found cached.
def checkcache(filename=None, use_linecache_lines=False):
    
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
                pass
            pass
        pass
    return result

def cache(filename, reload_on_change=False):
    '''Cache filename if it's not already cached.
    Return the expanded filename for it in the cache
    or nil if we can't find the file.'''
    if filename in file_cache:
        if reload_on_change: checkcache(filename)
        pass
    else:
        update_cache(filename, True)
        pass
    if filename in file_cache:
      return file_cache[filename].path
    else: return None
    return # Not reached

def is_cached(filename):
    '''Return True if filename is cached'''
    return unmap_file(filename) in file_cache

def is_empty(filename):
    filename=unmap_file(filename)
    return 0 == len(file_cache[filename].lines)

def getline(filename, line_number, reload_on_change=True):
    '''Get line `line_number' from file named `filename'. Return nil if
    there was a problem. If a file named filename is not found, the
    function will look for it in the sys.path array.
    
    Examples:

    lines = pyficache.getline('/tmp/myfile.py')
    # Same as above
    sys.path.append('/tmp')
    lines = pyficache.getlines('myfile.py')
    '''
    filename = unmap_file(filename)
    filename, line_number = unmap_file_line(filename, line_number)
    lines = getlines(filename, reload_on_change)
    if lines and line_number >=1 and line_number < len(lines):
        return lines[line_number-1].rstrip('\n')
    else:
        return None
    return # Not reached

def getlines(filename, reload_on_change=False):
    '''Read lines of `filename' and cache the results. However
    `filename' was previously cached use the results from the
    cache. Return None if we can't get lines'''
    filename = unmap_file(filename)
    if reload_on_change: checkcache(filename) 
    if filename in file_cache:
        return file_cache[filename].lines
    else:
        update_cache(filename, True)
        pass
    if filename in file_cache:
        return file_cache[filename].lines 
    return None

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
    if isinstance(types.IntType, line_range):
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
    for line in file_cache[filename].lines:
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
    return len(file_cache[filename].lines)

def stat(filename, use_cache_only=False):
    '''Return stat() info for `filename'. If `use_cache_only' is False,
    we'll try to fetch the file if it is not cached.'''
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
        e.line_numbers = coverage.the_coverage.analyze_morf(fullname)[1]
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
            return [from_file, start+line-line_range.begin] 
        pass
    return [filename, line]

def update_cache(filename, use_linecache_lines=False):
    '''Update a cache entry.  If something's wrong, return
    None. Return True if the cache was updated and False if not.  If
    use_linecache_lines is True, use an existing cache entry as source
    for the lines of the file.'''
    
    if not filename: return None

    if filename in file_cache: del file_cache[filename]
    path = os.path.abspath(filename)
    
    if use_linecache_lines:
      fname_list = [filename]
      if file2file_remap.get(path):
          fname_list.append(file2file_remap[path]) 
          for filename in fname_list:
              lines = linecache.getlines(filename)
              try:
                  stat = os.stat(filename)
              except:
                  stat = None
                  pass
              pass
          file_cache[filename] = LineCacheInfo(stat, None, lines, path, 
                                               None)
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
      lines = fp.readlines()
      fp.close()
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

  update_cache('os')

  lines = getlines(__file__)
  print "%s has %s lines" % (__file__, len(lines))
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
  checkcache() # Check all files in the cache
  clear_file_cache()
  print("%s is now %scached." % (__file__, yes_no(is_cached(__file__))))
#   # digest = SCRIPT_LINES__.select{|k,v| k =~ /digest.rb$/}
#   # if digest is not None: print digest.first[0]
#   line = getline(__file__, 7)
#   print "The 7th line is\n%s" % line
  # remap_file_lines(__file__, 'test2', [10..20], 6)
  # print getline('test2', 10)
  # print "Remapped 10th line of test2 is\n%s" % line
        
