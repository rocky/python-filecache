#
"Unit test for remapping lines pyficache (pytest version)"
import os.path as osp
from pyficache import getline

TEST_DIR = osp.abspath(osp.dirname(__file__))


def test_remap():
    pyasm_path = osp.join(TEST_DIR, "seven-313.pyasm")
    line = getline(pyasm_path, 2)
    expected_line2 = "  2:           2 |67 01| RETURN_CONST         (7)\n"
    assert line == expected_line2
