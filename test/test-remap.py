#!/usr/bin/env python
'Unit test for remapping lines pyficache'
import os, re, sys, unittest

import os.path as osp
TEST_DIR = osp.abspath(osp.dirname(__file__))
top_builddir = osp.join(TEST_DIR, '..')
if top_builddir[-1] != osp.sep:
    top_builddir += osp.sep
sys.path.insert(0, top_builddir)

from pyficache import remap_file_lines, getline

# Test File Line remapping
def strip_line(line):
    return re.split('[#;]', line)[0].strip()


class TestRemapLines(unittest.TestCase):

    def test_remap(self):
        mapped_path = os.path.join(TEST_DIR, 'mapped.py')
        unmapped_path = os.path.join(TEST_DIR, 'unmapped.py')
        fp = open(unmapped_path, 'r')
        unmapped_lines = fp.readlines()
        fp.close()
        mapping = ((1, 3), (4, 5))
        remap_file_lines(unmapped_path, mapped_path, mapping)

        # We'll use reversed just to be a little more devious
        for unmapped_no, mapped_no in reversed(mapping):
            unmapped_line = strip_line(unmapped_lines[unmapped_no-1])
            mapped_line = strip_line(getline(mapped_path, mapped_no))
            self.assertEqual(unmapped_line, mapped_line,
                        'We should get exactly the same lines as '
                        'reading this file.')


        # Now try mappings outside of the ones specifically listed
        for unmapped_no, mapped_no in ((5,6),):
            unmapped_line = strip_line(unmapped_lines[unmapped_no-1])
            mapped_line = strip_line(getline(mapped_path, mapped_no))
            self.assertEqual(unmapped_line, mapped_line,
                        'We should get exactly the same lines as '
                        'reading this file.')
    pass

if __name__ == '__main__':
    unittest.main()
