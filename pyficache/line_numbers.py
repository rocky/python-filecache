from xdis import findlinestarts, iscode, load_file
from collections import deque

def code_linenumbers_in_file(filename):
    # FIXME: try to find bytecode for corresponding file
    code = load_file(filename)
    return code_loop(code)

def code_loop(code):
    """Accumulates list of line numbers found in co by looking for code objects
    in code.
    """

    queue = deque([code])
    line_numbers = set()
    while len(queue) > 0:
        code = queue.popleft()
        line_numbers.update([tup[1] for tup in findlinestarts(code)])
        for c in code.co_consts:
            if iscode(c):
                queue.append(c)
            pass
        pass
    return line_numbers

if __name__ == "__main__":
    print(code_linenumbers_in_file(__file__))
