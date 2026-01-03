#
"Unit test for remapping lines pyficache (pytest version)"
import os
import re
import os.path as osp

TEST_DIR = osp.abspath(osp.dirname(__file__))
top_builddir = osp.join(TEST_DIR, "..")

from pyficache import add_remap_pat, getline, remap_file_lines, remap_file_pat


def strip_line(line):
    return re.split("[#;]", line)[0].strip()


def test_remap():
    mapped_path = os.path.join(TEST_DIR, "mapped.py")
    unmapped_path = os.path.join(TEST_DIR, "unmapped.py")

    with open(unmapped_path, "r") as fp:
        unmapped_lines = fp.readlines()

    mapping = ((1, 3), (4, 5))
    remap_file_lines(unmapped_path, str(mapped_path), mapping)

    # # We'll use reversed just to be a little more devious
    # for unmapped_no, mapped_no in reversed(mapping):
    #     unmapped_line = strip_line(unmapped_lines[unmapped_no - 1])
    #     mapped_line = strip_line(getline(str(mapped_path), mapped_no))
    #     assert unmapped_line == mapped_line, (
    #         "We should get exactly the same lines as reading this file."
    #     )

    # # Now try mappings outside of the ones specifically listed
    # for unmapped_no, mapped_no in ((5, 6),):
    #     unmapped_line = strip_line(unmapped_lines[unmapped_no - 1])
    #     mapped_line = strip_line(getline(str(mapped_path), mapped_no))
    #     assert unmapped_line == mapped_line, (
    #         "We should get exactly the same lines as reading this file."
    #     )

    # remapping by pattern
    add_remap_pat("^/code", "/tmp/project")
    assert remap_file_pat("/code/setup.py") == "/tmp/project/setup.py"
