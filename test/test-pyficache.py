#!/usr/bin/env python
# Note: the next line has to be at line 3 for testing. We introspect on this source.
# This is line 3.
"""
Unit test for pyficache
"""
from __future__ import with_statement
from xdis import PYTHON_VERSION, PYTHON3
import os, sys, unittest
from tempfile import mkstemp

import os.path as osp

TEST_DIR = osp.abspath(osp.dirname(__file__))

top_builddir = osp.join(TEST_DIR, "..")
if top_builddir[-1] != osp.sep:
    top_builddir += osp.sep
sys.path.insert(0, top_builddir)

import pyficache
from pyficache import PYVER

# Test LineCache module
class TestPyFiCache(unittest.TestCase):
    def setUp(self):
        pyficache.clear_file_cache()
        return

    def test_basic(self):
        filename = __file__
        if ".pyc" == filename[-4:]:
            filename = filename[:-1]
            pass

        fp = open(filename, "r")
        compare_lines = fp.readlines()
        self.assertTrue(
            compare_lines, "Should have been able to read %s for comparing" % filename
        )
        fp.close()

        # Test getlines to read this file.
        lines = pyficache.getlines(__file__)
        self.assertEqual(
            compare_lines,
            lines,
            "We should get exactly the same lines as " "reading this file.",
        )

        # Test getline to read this file. The file should now be cached,
        # so internally a different set of routines are used.
        test_line = 3
        line = pyficache.getline(__file__, test_line, {"strip_nl": False})
        self.assertEqual(
            compare_lines[test_line - 1],
            line,
            "We should get exactly the same line as reading " "this file.",
        )
        line = pyficache.getline(__file__, test_line, {"output": "light"})
        self.assertTrue(
            line.index("# This is line 3.") >= 0,
            (
                "Terminal formatted line 3 should be '# This is line 3.', got:\n%s"
                % line
            ),
        )

        # Test getting the line via a relative file name
        old_dir = os.getcwd()
        os.chdir(osp.dirname(osp.abspath((__file__))))
        short_file = osp.basename(__file__)
        test_line = 10
        line = pyficache.getline(short_file, test_line, {"strip_nl": False})
        self.assertEqual(
            compare_lines[test_line - 1],
            line,
            "Short filename lookup on %s should work" % short_file,
        )
        os.chdir(old_dir)

        # Write a temporary file; read contents, rewrite it and check that
        # we get a change when calling getline.
        (fd, path) = mkstemp(prefix="pyfcache", suffix=".txt")
        test_string = "Now is the time.\n"
        with open(path, "w") as f:
            f.write(test_string)
            f.close()
            pass
        line = pyficache.getline(path, 1, {"strip_nl": False})
        self.assertEqual(
            test_string, line, "C'mon - a simple line test like this worked " "before."
        )
        with open(path, "w") as f:
            test_string = "Now is another time."
            f.write(test_string)
            f.close()
            pass

        pyficache.checkcache()
        line = pyficache.getline(path, 1)
        self.assertEqual(
            test_string, line, "checkcache should have reread the temporary file."
        )
        try:
            os.remove(path)
        except:
            pass
        return

    def test_cached(self):
        myfile = __file__
        self.assertEqual(
            False,
            pyficache.is_cached(myfile),
            ("file %s shouldn't be cached - just cleared cache." % myfile),
        )
        line = pyficache.getline(__file__, 1)
        assert line
        self.assertEqual(
            True,
            pyficache.is_cached(__file__),
            "file %s should now be cached" % __file__,
        )
        # self.assertEqual(false, pyficache.cached_script?('./short-file'),
        #              "Should not find './short-file' in SCRIPT_LINES__")
        # self.assertEqual(True, 78 < pyficache.size(__file__))

        # Unlike Ruby, Python doesn't have SCRIPT_LINES__
        # old_dir = os.getcwd()
        # os.chdir(osp.dirname(osp.abspath((__file__))))
        # load('./short-file', 0)
        # self.assertEqual(True, pyficache.cached_script?('./short-file'),
        #                "Should be able to find './short-file' "
        #                "in SCRIPT_LINES__")
        # os.chdir(old_dir)
        return

    def test_remap(self):
        pyficache.remap_file(__file__, "another-name")
        line1 = pyficache.getline("another-name", 1)
        line2 = pyficache.getline(__file__, 1)
        self.assertEqual(line1, line2, "Both lines should be the same via remap_file")
        filename = pyficache.remove_remap_file("another-name")
        self.assertEqual(filename, __file__)
        filename = pyficache.remove_remap_file("another-name")
        self.assertEqual(filename, None)
        return

    def test_uncache(self):
        self.assertEqual(
            pyficache.uncache_script("<script>"), None, "<script should not be cached"
        )

        return

    def test_remap_lines(self):
        pyficache.remap_file_lines(__file__, "test2", ((6, 10),))

        line5 = pyficache.getline(__file__, 5)
        pyficache.remap_file_lines(__file__, "test2", ((5, 9),))
        rline9 = pyficache.getline("test2", 9)
        self.assertEqual(
            line5,
            rline9,
            "lines should be the same via remap_file_line - " "remap integer",
        )

        line6 = pyficache.getline(__file__, 6)
        rline10 = pyficache.getline("test2", 10)
        self.assertEqual(
            line6, rline10, "lines should be the same via remap_file_line - " "range"
        )

        line7 = pyficache.getline(__file__, 7)
        rline11 = pyficache.getline("test2", 11)
        self.assertEqual(
            line7, rline11, "lines should be the same via remap_file_line - " "range"
        )

        # line8 = pyficache.getline(__file__, 8)
        # pyficache.remap_file_lines(__file__, __file__, ((8, 20),))
        # rline20 = pyficache.getline(__file__, 20)
        # self.assertEqual(line8, rline20,
        #                  'lines should be the same via remap_file_line - '
        #                  'None file')
        return

    def test_path(self):
        self.assertEqual(
            None,
            pyficache.path(__file__),
            ("path for %s should be None - " "just cleared cache." % __file__),
        )
        path = pyficache.cache_file(__file__)
        self.assertTrue(path, "should have cached path for %s" % __file__)
        # self.assertEqual(
        #     path,
        #     pyficache.path(__file__),
        #     (
        #         "path %s of %s should be the same as we got "
        #         "before (%s)" % (path, __file__, pyficache.path(__file__))
        #     ),
        # )
        return

    def test_trace_line_numbers(self):
        test_file = osp.join(TEST_DIR, "short-file")
        line_nums = pyficache.trace_line_numbers(test_file)
        if 0 == len(line_nums):
            self.assertEqual({}, line_nums)
        else:
            self.assertEqual(set([1]), line_nums)
            pass
        test_file = osp.join(TEST_DIR, "devious.py")
        if PYTHON_VERSION < 3.0 or PYTHON_VERSION in (3.1, 3.2, 3.3, 3.4, 3.5, 3.6):
            expected = [4, 6, 8, 9]
        elif PYTHON_VERSION >= 3.8:
            expected = [2, 5, 7, 9]
        else:
            expected = [4, 5, 8, 9]
        self.assertEqual(set(expected), pyficache.trace_line_numbers(test_file))
        return

    # def test_universal_new_lines(self):
    #     test_file = osp.join(TEST_DIR, 'dos-file')
    #     lines = pyficache.getlines(test_file)
    #     self.assertEqual(lines, ['Foo\n', 'bar\n', 'baz\n'])
    #     # self.assertTrue(test_file in pyficache.file_cache)
    #     file_obj = pyficache.file_cache[test_file]
    #     # self.assertEqual('\r\n', file_obj.eols)

    #     test_file = osp.join(TEST_DIR, 'mixed-eol-file')
    #     lines = pyficache.getlines(test_file)
    #     self.assertEqual(lines, ['Unix\n', 'DOS\n', 'unix\n'])
    #     self.assertTrue(test_file in pyficache.file_cache)
    #     file_obj = pyficache.file_cache[test_file]
    #     self.assertEqual(('\n', '\r\n'), file_obj.eols)

    def test_sha1(self):
        global TEST_DIR
        test_file = osp.join(TEST_DIR, "short-file")
        self.assertEqual(
            "1134f95ea84a3dcc67d7d1bf41390ee1a03af6d2", pyficache.sha1(test_file)
        )
        return

    def test_size(self):
        global TEST_DIR
        test_file = osp.join(TEST_DIR, "short-file")
        self.assertEqual(2, pyficache.size(test_file))
        return

    def test_stat(self):
        self.assertEqual(
            None,
            pyficache.stat(__file__, use_cache_only=True),
            ("stat for %s should be None - " "just cleared cache." % __file__),
        )
        line = pyficache.getline(__file__, 1)
        self.assertTrue(line)
        self.assertTrue(
            pyficache.stat(__file__), "file %s should now have a stat" % __file__
        )
        return

    def test_update_cache(self):
        self.assertFalse(pyficache.update_cache("foo"))
        self.assertTrue(pyficache.update_cache(__file__))
        return

    def test_clear_file_cache(self):
        pyficache.update_cache(__file__)
        pyficache.clear_file_format_cache()
        pyficache.clear_file_cache()
        self.assertEqual([], pyficache.cached_files())
        return

    def test_resolve_name_to_path(self):
        if PYTHON3:
            testdata = (
                ("pyc/__pycache__/foo.cpython-%s.pyc" % PYVER, "pyc/foo.py"),
                ("__pycache__/pyo.cpython-%s.pyc" % PYVER, "pyo.py"),
                ("foo/__pycache__/bar.cpython-%s.pyo" % PYVER, "foo/bar.py"),
            )
        else:
            testdata = (
                ("pyc/foo.pyc", "pyc/foo.py"),
                ("pyo.pyc", "pyo.py"),
                ("foo.pyo", "foo.py"),
            )
        for path, expect in testdata:
            self.assertEqual(pyficache.resolve_name_to_path(path), expect)
        return

    pass


if __name__ == "__main__":
    unittest.main()
