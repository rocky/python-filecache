#!/usr/bin/env python
'Unit test for pyficache'
import inspect, os, sys, unittest
top_builddir = os.path.join(os.path.dirname(__file__), '..')
if top_builddir[-1] != os.path.sep:
    top_builddir += os.path.sep
sys.path.insert(0, top_builddir)

TEST_DIR = os.path.dirname(__file__)

import pyficache

# Test LineCache module
class TestPyFiCache(unittest.TestCase):

  def setUp(self):
      pyficache.clear_file_cache()
      return
  
  def test_basic(self):
      fp = open(__file__, 'r')
      compare_lines = fp.readlines()
      fp.close()
    
      # Test getlines to read this file.
      lines = pyficache.getlines(__file__)
      self.assertEqual(compare_lines, lines,
                       'We should get exactly the same lines as reading this file.')
    
#       # Test getline to read this file. The file should now be cached,
#       # so internally a different set of routines are used.
#       test_line = 1
#       line = pyficache.getline(__file__, test_line)
#       self.assertEqual(compare_lines[test_line-1], line,
#                        'We should get exactly the same line as reading this file.')
    
#       # Test getting the line via a relative file name
#       Dir.chdir(os.path.dirname(__file__)) do 
#       short_file = os.path.basename(__file__)
#       test_line = 10
#       line = pyficache.getline(short_file, test_line)
#       self.assertEqual(compare_lines[test_line-1], line,
#                    'Short filename lookup should work')
  
#       # Write a temporary file; read contents, rewrite it and check that
#       # we get a change when calling getline.
#       tf = Tempfile.new("testing")
#       test_string = "Now is the time.\n"
#       tf.puts(test_string)
#       tf.close()
#       line = pyficache.getline(tf.path, 1)
#       self.assertEqual(test_string, line,
#                        "C'mon - a simple line test like this worked before.")
#       tf.open()
#       test_string = "Now is another time.\n"
#       tf.puts(test_string)
#       tf.close()
#       pyficache.checkcache()
#       line = pyficache.getline(tf.path, 1)
#       self.assertEqual(test_string, line,
#                        "checkcache should have reread the temporary file.")
#       FileUtils.rm tf.path
      
#       pyficache.update_cache(__file__)
#       pyficache.clear_file_cache
#       return

#   def test_cached(self):
#     self.assertEqual(false, pyficache.is_cached(__file__),
#                      ("file %s shouldn't be cached - just cleared cache."
#                      % __file__))
#     line = pyficache.getline(__file__, 1)
#     assert line
#     self.assertEqual(true, pyficache.is_cached(__file__),
#                  "file #{__file__} should now be cached")
#     self.assertEqual(false, pyficache.cached_script?('./short-file'),
#                  "Should not find './short-file' in SCRIPT_LINES__")
#     self.assertEqual(true, 78 < LineCache.size(__file__))
#     Dir.chdir(os.dir.dirname(__file__)) do 
#       load('./short-file', 0)
#       self.assertEqual(true, pyficache.cached_script?('./short-file'),
#                    "Should be able to find './short-file' in SCRIPT_LINES__")
#     end
#     return

#   def test_remap(self):
#     pyficache.remap_file(__file__, 'another-name')
#     line1 = pyficache.getline('another-name', 1)
#     line2 = pyficache.getline(__file__, 1)
#     self.assertEqual(line1, line2, 'Both lines should be the same via remap_file')
#     return

#   def test_remap_lines(self):
#     pyficache.remap_file_lines(__file__, 'test2', (10..11), 6)

#     line5 = pyficache.getline(__file__, 5)
#     pyficache.remap_file_lines(__file__, 'test2', 9, 5)
#     rline9  = pyficache.getline('test2', 9)
#     self.assertEqual(line5, rline9, 
#                  'lines should be the same via remap_file_line - remap integer')

#     line6 = pyficache.getline(__file__, 6)
#     rline10 = pyficache.getline('test2', 10)
#     self.assertEqual(line6, rline10, 
#                  'lines should be the same via remap_file_line - range')

#     line7 = pyficache.getline(__file__, 7)
#     rline11 = pyficache.getline('test2', 11)
#     self.assertEqual(line7, rline11, 
#                  'lines should be the same via remap_file_line - range')

#     line8 = pyficache.getline(__file__, 8)
#     pyficache.remap_file_lines(__file__, None, 20, 8)
#     rline20 = pyficache.getline(__file__, 20)
#     self.assertEqual(line8, rline20, 
#                  'lines should be the same via remap_file_line - None file')
#     return

  def test_path(self):
    self.assertEqual(None, pyficache.path(__file__),
                     ("path for %s should be None - just cleared cache." %
                      __file__))
    path = pyficache.cache(__file__)
    self.assertTrue(path)
    self.assertEqual(path, pyficache.path(__file__),
                     ("path %s of %s should be the same as we got before (%s)" %
                      (path, __file__, pyficache.path(__file__))))
    return

  def test_trace_line_numbers(self):
    test_file = os.path.join(TEST_DIR, 'short-file')
    self.assertEqual([], pyficache.trace_line_numbers(test_file))
    test_file = os.path.join(TEST_DIR, 'devious.py')
    self.assertEqual([2, 5, 7, 9], pyficache.trace_line_numbers(test_file))
    return

  def test_sha1(self):
      global TEST_DIR
      test_file = os.path.join(TEST_DIR, 'short-file') 
      self.assertEqual('1134f95ea84a3dcc67d7d1bf41390ee1a03af6d2',
                       pyficache.sha1(test_file))
      return

  def test_size(self):
      global TEST_DIR
      test_file = os.path.join(TEST_DIR, 'short-file') 
      self.assertEqual(2, pyficache.size(test_file))
      return

  def test_stat(self):
      self.assertEqual(None, pyficache.stat(__file__, use_cache_only=True),
                       ("stat for %s should be None - just cleared cache." %
                        __file__))
      line = pyficache.getline(__file__, 1)
      self.assertTrue(line)
      self.assertTrue(pyficache.stat(__file__),
                      "file %s should now have a stat" % __file__ )
      return

  pass
if __name__ == '__main__':
    unittest.main()
