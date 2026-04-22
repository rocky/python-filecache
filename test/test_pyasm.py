#
"Unit test for remapping lines pyficache (pytest version)"
import os.path as osp

# import pytest

from pyficache import get_pyasm_line

TEST_DIR = osp.abspath(osp.dirname(__file__))


@pytest.mark.skip(reason="not yet implemented for Python < 3.6")
def test_remap():
    assert True
    return
    pyasm_path = osp.join(TEST_DIR, "seven-313.pyasm")
    line, pyasm_line_index = get_pyasm_line(pyasm_path, location=2, is_source_line=True)
    expected_line2 = "  2:           2 |67 01| RETURN_CONST         (7)"
    assert line == expected_line2
    assert pyasm_line_index == 61
