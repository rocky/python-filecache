# -*- coding: utf-8 -*-
#
#   Copyright (C) 2025 Rocky Bernstein <rocky@gnu.org>
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

from collections import defaultdict

from types import CodeType
from typing import Dict, Optional

from xdis import iscode, load_file, findlinestarts
from collections import deque


class CodePositionInfo:
    """
    lineno_and_offset: A dictionary mapping line and code offset numbers into a pair of
          (starting line, starting column), (ending line, ending column) values.
          in code.

    parent: static enclosing code or not None if this a module.
    """

    lineno_and_offset = None
    parent = None

    def __init__(self, lineno_and_offset=None, parent=None):
        self.lineno_and_offset = lineno_and_offset
        self.parent = parent


# A cache of source-code position and code offset information keyed by a Python code object.
code_position_cache: Dict[CodeType, CodePositionInfo] = {}


def update_code_position_cache(filename: str) -> Dict[int, list]:
    """Update code_position_cache and returns a dictionary mapping line number in a file to its
    offsets in a code object.  Note for example that loops and
    conditional statements typically have more than one offset
    associated with a line number.

    The line number is used as a key to support validating lookup by line
    number which occurs in setting a breakpoint in a debugger.

    When the code offset is 0, store the code object. This is a
    situation where a line number itself is ambiguous and can refer
    to several scopes. The code object as opposed to its name,
    might be useful in setting breakpoints.
    """
    # FIXME: try to find bytecode for corresponding file
    code = load_file(filename)
    return code_loop_for_positions(code)


def code_loop_for_positions(
    code: CodeType,
) -> Dict[int, list]:
    """Loops over all code objects found within the constant section of `code` returning the
    information described in populate_code_position_cache() above and updating code_position_cache.
    """

    parent: Optional[CodeType] = None
    queue = deque([(code, parent)])

    offset_line_dict = {}
    line_offset_dict = {}
    line_info = defaultdict(list)

    while len(queue) > 0:
        code, parent = queue.popleft()

        for offset, line in findlinestarts(code):
            offset_line_dict[offset] = line
            line_offset_dict[line] = offset

        # First, process code.co_lines()...
        for start_offset, lineno in findlinestarts(code):
            if start_offset in offset_line_dict:
                line_info[lineno].append((code, start_offset))

        for c in code.co_consts:
            if iscode(c):
                queue.append((c, code))
            pass
        pass

    return line_info


if __name__ == "__main__":
    from pprint import pformat

    lineno_info = update_code_position_cache(__file__)

    for line_number, offset_pairs in lineno_info.items():
        print(f"line #: {line_number}")
        print(
            "  "
            + ", ".join([f"{code.co_name}: {offset}" for code, offset in offset_pairs])
        )
        print()

    for code, code_position_info in code_position_cache.items():
        print("=" * 30)
        print(f"{code.co_name} parent: {code_position_info.parent}")
        print(
            f"(line, offset): source positions for {code.co_name}:"
            f"\n\t{pformat(code_position_info.lineno_and_offset)}"
        )
        print(
            f"(line, offset): start columns for {code.co_name}:"
            f"\n\t{pformat(code_position_info.lineno_and_start_column)}"
        )
        print("-" * 30)
