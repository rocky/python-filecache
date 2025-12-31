#
# Note: the next line has to be at line 3 for testing. We introspect on this source.
# This is line 3.
"""
Unit test for pyficache (pytest version)
"""

import os
import os.path as osp
import platform
import sys
from tempfile import mkstemp

import pytest
from xdis.version_info import PYTHON3, PYTHON_VERSION_TRIPLE

import pyficache
from pyficache import PYVER

TEST_DIR = osp.abspath(osp.dirname(__file__))

top_builddir = osp.join(TEST_DIR, "..")
if top_builddir[-1] != osp.sep:
    top_builddir += osp.sep
sys.path.insert(0, top_builddir)


@pytest.fixture(autouse=True)
def clear_file_cache():
    # runs before each test
    pyficache.clear_file_cache()
    yield
    # no teardown actions required


class TestPyFiCache:
    def test_basic(self):
        filename = __file__
        if ".pyc" == filename[-4:]:
            filename = filename[:-1]

        fp = open(filename, "r")
        compare_lines = fp.readlines()
        assert compare_lines, f"Should have been able to read {filename} for comparing"
        fp.close()

        # Test getlines to read this file.
        lines = pyficache.getlines(__file__)
        assert (
            compare_lines == lines
        ), "We should get exactly the same lines as reading this file."

        # Test getline to read this file. The file should now be cached,
        # so internally a different set of routines are used.
        test_line = 3
        line = pyficache.getline(__file__, test_line, {"strip_nl": False})
        assert (
            compare_lines[test_line - 1] == line
        ), "We should get exactly the same line as reading this file."

        line = pyficache.getline(__file__, test_line, {"output": "light"})
        assert (
            "# This is line 3." in line
        ), f"Terminal formatted line 3 should be '# This is line 3.', got:\n{line}"

        # Test getting the line via a relative file name
        old_dir = os.getcwd()
        os.chdir(osp.dirname(osp.abspath((__file__))))
        short_file = osp.basename(__file__)
        test_line = 10
        line = pyficache.getline(short_file, test_line, {"strip_nl": False})
        assert (
            compare_lines[test_line - 1] == line
        ), f"Short filename lookup on {short_file} should work"
        os.chdir(old_dir)

        # Write a temporary file; read contents, rewrite it and check that
        # we get a change when calling getline.
        (fd, path) = mkstemp(prefix="pyfcache", suffix=".txt")
        os.close(fd)
        test_string = "Now is the time.\n"
        with open(path, "w") as f:
            f.write(test_string)

        line = pyficache.getline(path, 1, {"strip_nl": False})
        assert (
            test_string == line
        ), "C'mon - a simple line test like this worked before."

        with open(path, "w") as f:
            test_string = "Now is another time."
            f.write(test_string)

        pyficache.checkcache()
        line = pyficache.getline(path, 1)
        assert test_string == line, "checkcache should have reread the temporary file."
        try:
            os.remove(path)
        except Exception:
            pass

    def test_cached(self):
        myfile = __file__
        assert (
            pyficache.is_cached(myfile) is False
        ), f"file {myfile} shouldn't be cached - just cleared cache."

        line = pyficache.getline(__file__, 1)
        assert line
        assert (
            pyficache.is_cached(__file__) is True
        ), f"file {__file__} should now be cached"

    def test_remap(self):
        pyficache.remap_file(__file__, "another-name")
        line1 = pyficache.getline("another-name", 1)
        line2 = pyficache.getline(__file__, 1)
        assert line1 == line2, "Both lines should be the same via remap_file"

        filename = pyficache.remove_remap_file("another-name")
        assert filename == __file__

        filename = pyficache.remove_remap_file("another-name")
        assert filename is None

    def test_uncache(self):
        assert (
            pyficache.uncache_script("<script>") is None
        ), "<script should not be cached"

    # FIXME:
    # def test_remap_lines(self):
    #     pyficache.remove_remap_file(__file__)
    #     pyficache.remap_file_lines(__file__, __file__, ((6, 10),))

    #     line5 = pyficache.getline(__file__, 5)
    #     pyficache.remap_file_lines(__file__, __file__, ((5, 9),))
    #     rline9 = pyficache.getline(__file__, 9)
    #     assert line5 == rline9, "lines should be the same via remap_file_line - remap integer"

    #     line6 = pyficache.getline(__file__, 6)
    #     rline10 = pyficache.getline("test2", 10)
    #     assert line6 == rline10, "lines should be the same via remap_file_line - range"

    #     line7 = pyficache.getline(__file__, 7)
    #     rline11 = pyficache.getline("test2", 11)
    #     assert line7 == rline11, "lines should be the same via remap_file_line - range"

    def test_path(self):
        assert (
            pyficache.path(__file__) is None
        ), f"path for {__file__} should be None - just cleared cache."
        path = pyficache.cache_file(__file__)
        assert path, f"should have cached path for {__file__}"

    def test_trace_line_numbers(self):
        test_file = osp.join(TEST_DIR, "short-file")
        line_nums = pyficache.trace_line_numbers(test_file)
        assert line_nums is not None, "expected to get line numbers from pyficache"
        if 0 == len(line_nums):
            assert line_nums == {}
        else:
            if platform.python_implementation() == "GraalVM":
                start_lineno = 2
            else:
                start_lineno = 1 if PYTHON_VERSION_TRIPLE < (3, 11) else 0
            assert set([start_lineno]) == line_nums

        test_file = osp.join(TEST_DIR, "devious.py")
        expected = {0, 2, 5, 7, 9}
        assert expected == pyficache.trace_line_numbers(test_file)

    def test_sha1(self):
        test_file = osp.join(TEST_DIR, "short-file")
        assert pyficache.sha1(test_file) == "1134f95ea84a3dcc67d7d1bf41390ee1a03af6d2"

    def test_size(self):
        test_file = osp.join(TEST_DIR, "short-file")
        assert pyficache.size(test_file) == 2

    def test_stat(self):
        assert (
            pyficache.stat(__file__, use_cache_only=True) is None
        ), f"stat for {__file__} should be None - just cleared cache."
        line = pyficache.getline(__file__, 1)
        assert line
        assert pyficache.stat(__file__), f"file {__file__} should now have a stat"

    def test_update_cache(self):
        assert pyficache.update_cache("foo") is False
        assert pyficache.update_cache(__file__) is True

    def test_clear_file_cache(self):
        pyficache.update_cache(__file__)
        pyficache.clear_file_format_cache()
        pyficache.clear_file_cache()
        assert pyficache.cached_files() == []

    def test_resolve_name_to_path(self):
        if PYTHON3:
            testdata = (
                (f"pyc/__pycache__/foo.cpython-{PYVER}.pyc", osp.join("pyc", "foo.py")),
                (f"__pycache__/pyo.cpython-{PYVER}.pyc", "pyo.py"),
                (f"foo/__pycache__/bar.cpython-{PYVER}.pyo", osp.join("foo", "bar.py")),
            )
        else:
            testdata = (
                (osp.join("pyc", "foo.pyc"), osp.join("pyc", "foo.py")),
                ("pyo.pyc", "pyo.py"),
                ("foo.pyo", "foo.py"),
            )
        for path, expect in testdata:
            assert pyficache.resolve_name_to_path(path) == expect
