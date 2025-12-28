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
from typing import Dict, Tuple

from xdis import iscode, load_file, findlinestarts
from collections import deque


def get_position_info(
    filename,
) -> Tuple[Dict[int, list], Dict[Tuple[int, int], set], Dict[Tuple[int, int], set]]:
    """Returns three things:

    1) a dictionary mapping line number in a file to its
    offsets in a code object.  Note for example that loops and
    conditional statements typically have more than one offset
    associated with a line number.

    The line number is used as a key to support validating lookup by line
    number which occurs in setting a breakpoint in a debugger.

    When the code offset is 0, store the code object. This is a
    situation where a line number itself is ambiguous and can refer
    to several scopes. The code object as opposed to its name,
    might be useful in setting breakpoints.

    2) A dictionary mapping line and code offset numbers into a pair of
      (starting line, starting column), (ending line, ending column) values.
      in code.

    3) A dictionary mapping line and code offset numbers into a pair of
      (starting line, starting column), (ending line, ending column) values.
      in code.

    """
    # FIXME: try to find bytecode for corresponding file
    code = load_file(filename)
    return code_loop_for_positions(code)


def code_loop_for_positions(
    code: CodeType,
) -> Tuple[Dict[int, list], Dict[Tuple[int, int], set], Dict[Tuple[int, int], set]]:
    """Returns two dictionaries. The first dictionary maps line and code offset numbers into a pair of
      (starting line, starting column), (ending line, ending column) values.
    in code.
    """

    queue = deque([code])
    lineno_and_offset = {}
    lineno_and_start_column = {}
    line_info = defaultdict(list)
    while len(queue) > 0:
        code = queue.popleft()
        linestarts_dict = {line: offset for offset, line in findlinestarts(code)}
        for start_line, end_line, start_column, end_column in code.co_positions():
            start_offset = linestarts_dict.get(start_line, None)
            if (
                start_offset is not None
                and start_column is not None
                and end_column is not None
            ):
                lookup = (start_line, start_offset)
                if start_column == 0 and end_column == 0:
                    lineno_and_start_column[start_line, start_column] = (
                        start_offset,
                        code,
                    )
                else:
                    lineno_and_start_column[start_line, start_column] = start_offset

                    if existing_range := lineno_and_offset.get(lookup, False):
                        new_start = min(existing_range[0], (start_line, start_column))
                        new_stop = max(existing_range[1], (end_line, end_column))
                        lineno_and_offset[lookup] = (new_start, new_stop)
                    else:
                        lineno_and_offset[lookup] = (
                            (start_line, start_column),
                            (end_line, end_column),
                        )

        for start_offset, _, lineno in code.co_lines():
            if start_offset in linestarts_dict:
                # A start offset of 0 means that this code is at the
                # beginning of some module, method or function. This
                # is one place where it is possible for a line number
                # alone to be ambiguous about the scoping
                # level. Therefore, add in the code's qualified name,
                # co_qualname
                if start_offset == 0:
                    line_info[lineno].append(code)
                else:
                    line_info[lineno].append(start_offset)

        for c in code.co_consts:
            if iscode(c):
                queue.append(c)
            pass
        pass
    return line_info, lineno_and_offset, lineno_and_start_column


if __name__ == "__main__":
    from pprint import pp

    lineno_info, lineno_and_offset, lineno_and_start_column = get_position_info(
        __file__
    )
    pp(lineno_info)
    pp(lineno_and_offset)
    pp(lineno_and_start_column)
