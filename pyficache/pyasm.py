"""
Lexer for Python Disassembler Pyasm
"""

import re

from pygments.lexer import (
    RegexLexer,
    # include,
)

try:

    OPCODES = set([
        "ASYNC_GEN_WRAP",
        "BEFORE_ASYNC_WITH",
        "BEFORE_WITH",
        "BEGIN_FINALLY",
        "BINARY_ADD",
        "BINARY_AND",
        "BINARY_CALL",
        "BINARY_DIVIDE",
        "BINARY_FLOOR_DIVIDE",
        "BINARY_LSHIFT",
        "BINARY_MATRIX_MULTIPLY",
        "BINARY_MODULO",
        "BINARY_MULTIPLY",
        "BINARY_OP",
        "BINARY_OR",
        "BINARY_POWER",
        "BINARY_RSHIFT",
        "BINARY_SLICE",
        "BINARY_SUBSCR",
        "BINARY_SUBTRACT",
        "BINARY_TRUE_DIVIDE",
        "BINARY_XOR",
        "BREAK_LOOP",
        "BUILD_CLASS",
        "BUILD_CONST_KEY_MAP",
        "BUILD_FUNCTION",
        "BUILD_LIST",
        "BUILD_LIST_FROM_ARG",
        "BUILD_LIST_UNPACK",
        "BUILD_MAP",
        "BUILD_MAP_UNPACK",
        "BUILD_MAP_UNPACK_WITH_CALL",
        "BUILD_SET",
        "BUILD_SET_UNPACK",
        "BUILD_SLICE",
        "BUILD_STRING",
        "BUILD_TUPLE",
        "BUILD_TUPLE_UNPACK",
        "BUILD_TUPLE_UNPACK_WITH_CALL",
        "CACHE",
        "CALL",
        "CALL_FINALLY",
        "CALL_FUNCTION",
        "CALL_FUNCTION_EX",
        "CALL_FUNCTION_KW",
        "CALL_FUNCTION_VAR",
        "CALL_FUNCTION_VAR_KW",
        "CALL_INTRINSIC_1",
        "CALL_INTRINSIC_2",
        "CALL_KW",
        "CALL_METHOD",
        "CALL_METHOD_KW",
        "CHECK_EG_MATCH",
        "CHECK_EXC_MATCH",
        "CLEANUP_THROW",
        "COMPARE_OP",
        "CONTAINS_OP",
        "CONTINUE_LOOP",
        "CONVERT_VALUE",
        "COPY",
        "COPY_DICT_WITHOUT_KEYS",
        "COPY_FREE_VARS",
        "DELETE_ATTR",
        "DELETE_DEREF",
        "DELETE_FAST",
        "DELETE_GLOBAL",
        "DELETE_NAME",
        "DELETE_SLICE+0",
        "DELETE_SLICE+1",
        "DELETE_SLICE+2",
        "DELETE_SLICE+3",
        "DELETE_SLICE_0",
        "DELETE_SLICE_1",
        "DELETE_SLICE_2",
        "DELETE_SLICE_3",
        "DELETE_SUBSCR",
        "DICT_MERGE",
        "DICT_UPDATE",
        "DUP_TOP",
        "DUP_TOPX",
        "DUP_TOP_TWO",
        "END_ASYNC_FOR",
        "END_FINALLY",
        "END_FOR",
        "END_SEND",
        "ENTER_EXECUTOR",
        "EXEC_STMT",
        "EXIT_INIT_CHECK",
        "EXTENDED_ARG",
        "FORMAT_SIMPLE",
        "FORMAT_VALUE",
        "FORMAT_WITH_SPEC",
        "FOR_ITER",
        "FOR_LOOP",
        "GEN_START",
        "GET_AITER",
        "GET_ANEXT",
        "GET_AWAITABLE",
        "GET_ITER",
        "GET_LEN",
        "GET_YIELD_FROM_ITER",
        "IMPORT_FROM",
        "IMPORT_NAME",
        "IMPORT_STAR",
        "INPLACE_ADD",
        "INPLACE_AND",
        "INPLACE_DIVIDE",
        "INPLACE_FLOOR_DIVIDE",
        "INPLACE_LSHIFT",
        "INPLACE_MATRIX_MULTIPLY",
        "INPLACE_MODULO",
        "INPLACE_MULTIPLY",
        "INPLACE_OR",
        "INPLACE_POWER",
        "INPLACE_RSHIFT",
        "INPLACE_SUBTRACT",
        "INPLACE_TRUE_DIVIDE",
        "INPLACE_XOR",
        "INSTRUMENTED_CALL",
        "INSTRUMENTED_CALL_FUNCTION_EX",
        "INSTRUMENTED_CALL_KW",
        "INSTRUMENTED_END_FOR",
        "INSTRUMENTED_END_SEND",
        "INSTRUMENTED_FOR_ITER",
        "INSTRUMENTED_INSTRUCTION",
        "INSTRUMENTED_JUMP_BACKWARD",
        "INSTRUMENTED_JUMP_FORWARD",
        "INSTRUMENTED_LINE",
        "INSTRUMENTED_LOAD_SUPER_ATTR",
        "INSTRUMENTED_POP_JUMP_IF_FALSE",
        "INSTRUMENTED_POP_JUMP_IF_NONE",
        "INSTRUMENTED_POP_JUMP_IF_NOT_NONE",
        "INSTRUMENTED_POP_JUMP_IF_TRUE",
        "INSTRUMENTED_RESUME",
        "INSTRUMENTED_RETURN_CONST",
        "INSTRUMENTED_RETURN_VALUE",
        "INSTRUMENTED_YIELD_VALUE",
        "INTERPRETER_EXIT",
        "IS_OP",
        "JUMP",
        "JUMP_ABSOLUTE",
        "JUMP_BACKWARD",
        "JUMP_BACKWARD_NO_INTERRUPT",
        "JUMP_FORWARD",
        "JUMP_IF_FALSE",
        "JUMP_IF_FALSE_OR_POP",
        "JUMP_IF_NOT_DEBUG",
        "JUMP_IF_NOT_EXC_MATCH",
        "JUMP_IF_TRUE",
        "JUMP_IF_TRUE_OR_POP",
        "JUMP_NO_INTERRUPT",
        "KW_NAMES",
        "LIST_APPEND",
        "LIST_EXTEND",
        "LIST_TO_TUPLE",
        "LOAD_ASSERTION_ERROR",
        "LOAD_ATTR",
        "LOAD_BUILD_CLASS",
        "LOAD_CLASSDEREF",
        "LOAD_CLOSURE",
        "LOAD_CONST",
        "LOAD_DEREF",
        "LOAD_FAST",
        "LOAD_FAST_AND_CLEAR",
        "LOAD_FAST_CHECK",
        "LOAD_FAST_LOAD_FAST",
        "LOAD_FROM_DICT_OR_DEREF",
        "LOAD_FROM_DICT_OR_GLOBALS",
        "LOAD_GLOBAL",
        "LOAD_GLOBALS",
        "LOAD_LOCAL",
        "LOAD_LOCALS",
        "LOAD_METHOD",
        "LOAD_NAME",
        "LOAD_REVDB_VAR",
        "LOAD_SUPER_ATTR",
        "LOAD_SUPER_METHOD",
        "LOAD_ZERO_SUPER_ATTR",
        "LOAD_ZERO_SUPER_METHOD",
        "LOOKUP_METHOD",
        "MAKE_CELL",
        "MAKE_CLOSURE",
        "MAKE_FUNCTION",
        "MAP_ADD",
        "MATCH_CLASS",
        "MATCH_KEYS",
        "MATCH_MAPPING",
        "MATCH_SEQUENCE",
        "NOP",
        "POP_BLOCK",
        "POP_EXCEPT",
        "POP_FINALLY",
        "POP_JUMP_BACKWARD_IF_FALSE",
        "POP_JUMP_BACKWARD_IF_NONE",
        "POP_JUMP_BACKWARD_IF_NOT_NONE",
        "POP_JUMP_BACKWARD_IF_TRUE",
        "POP_JUMP_FORWARD_IF_FALSE",
        "POP_JUMP_FORWARD_IF_NONE",
        "POP_JUMP_FORWARD_IF_NOT_NONE",
        "POP_JUMP_FORWARD_IF_TRUE",
        "POP_JUMP_IF_FALSE",
        "POP_JUMP_IF_NONE",
        "POP_JUMP_IF_NOT_NONE",
        "POP_JUMP_IF_TRUE",
        "POP_TOP",
        "PRECALL",
        "PREP_RERAISE_STAR",
        "PRINT_EXPR",
        "PRINT_ITEM",
        "PRINT_ITEM_TO",
        "PRINT_NEWLINE",
        "PRINT_NEWLINE_TO",
        "PUSH_EXC_INFO",
        "PUSH_NULL",
        "RAISE_EXCEPTION",
        "RAISE_VARARGS",
        "RERAISE",
        "RESERVED",
        "RESERVE_FAST",
        "RESUME",
        "RETURN_CONST",
        "RETURN_GENERATOR",
        "RETURN_VALUE",
        "ROT_FOUR",
        "ROT_N",
        "ROT_THREE",
        "ROT_TWO",
        "SEND",
        "SETUP_ANNOTATIONS",
        "SETUP_ASYNC_WITH",
        "SETUP_CLEANUP",
        "SETUP_EXCEPT",
        "SETUP_FINALLY",
        "SETUP_LOOP",
        "SETUP_WITH",
        "SET_ADD",
        "SET_FUNCTION_ATTRIBUTE",
        "SET_FUNC_ARGS",
        "SET_LINENO",
        "SET_UPDATE",
        "SLICE+0",
        "SLICE+1",
        "SLICE+2",
        "SLICE+3",
        "SLICE_0",
        "SLICE_1",
        "SLICE_2",
        "SLICE_3",
        "STOP_CODE",
        "STORE_ANNOTATION",
        "STORE_ATTR",
        "STORE_DEREF",
        "STORE_FAST",
        "STORE_FAST_LOAD_FAST",
        "STORE_FAST_MAYBE_NULL",
        "STORE_FAST_STORE_FAST",
        "STORE_GLOBAL",
        "STORE_LOCALS",
        "STORE_MAP",
        "STORE_NAME",
        "STORE_SLICE",
        "STORE_SLICE+0",
        "STORE_SLICE+1",
        "STORE_SLICE+2",
        "STORE_SLICE+3",
        "STORE_SLICE_0",
        "STORE_SLICE_1",
        "STORE_SLICE_2",
        "STORE_SLICE_3",
        "STORE_SUBSCR",
        "SWAP",
        "TO_BOOL",
        "UNARY_CALL",
        "UNARY_CONVERT",
        "UNARY_INVERT",
        "UNARY_NEGATIVE",
        "UNARY_NOT",
        "UNARY_POSITIVE",
        "UNPACK_ARG",
        "UNPACK_EX",
        "UNPACK_LIST",
        "UNPACK_SEQUENCE",
        "UNPACK_TUPLE",
        "UNPACK_VARARG",
        "WITH_CLEANUP",
        "WITH_CLEANUP_FINISH",
        "WITH_CLEANUP_START",
        "WITH_EXCEPT_START",
        "YIELD_FROM",
        "YIELD_VALUE"]
    )

    can_pyasm = True
except ImportError:
    can_pyasm = False
    class RegexLexer(object):
        pass
    from pygments.lexers import GasLexer as PyasmLexer


class words(object):
    """
    Indicates a list of literal words that is transformed into an optimized
    regex that matches any of the words.

    .. versionadded:: 2.0
    """
    def __init__(self, words, prefix='', suffix=''):
        self.words = words
        self.prefix = prefix
        self.suffix = suffix


if can_pyasm:

    from pygments.token import (
        Comment,
        Name,
        Whitespace,
    )


    class PyasmLexer(RegexLexer):
        """
        For xdis's pydisasm.
        """

        name = "Pyasm"
        aliases = ["dis"]
        filenames = ["*.pyasm"]
        mimetypes = ["text/x-pyasm"]
        url = "https://pypi.org/project/xdis/"
        version_added = "1.00"

        char = r"[\w$.@-]"
        identifier = r"(?:[a-zA-Z$_]" + char + r"*|\." + char + "+)"
        number = r"(?:\d+)"

        user_defined_opcodes = set()

        def opcode_name_callback(self, match):
            opcode = match.group(0)
            self.user_defined_opcodes.add(opcode)
            yield match.start(), Name.Function, opcode


        tokens = {
            "root": [
                (r"\n", Whitespace),
                (number + ":", Name.Label),
                (r"#.*$", Comment.Single),
                # include("OPCODES"),
                # include("builtins"),
                # Add section names
                # # Section header
                # ('(Disassembly of section )(.*?)(:)$',
                #   bygroups(Text, Name.Label, Punctuation)),
            ],
            # "builtins": [
            #     (
            #         words(
            #             ("TOS",),
            #             prefix=r"\b",
            #             suffix=r"\b",
            #         ),
            #         Name.Builtin,
            #     ),
            # ],
            "whitespace": [
                (r"\n", Whitespace),
                (r"\s+", Whitespace),
                (r"([#]|//).*?\n", Comment.Single),
                (r"/[*][\w\W]*?[*]/", Comment.Multiline),
            ],
            # "OPCODES": [
            #     (r'[A-Z_a-z]\w*', opcode_name_callback, ('#pop', 'opcode type signatures')),
            #     (r'\n', Text, '#pop')
            # ],

        }

        def analyse_text(self, text):
            if re.search(r"^# pydisasm", text, re.M):
                return True


def compute_pyasm_line_mapping(pyasm_lines):
    r"""
    Build a from_to remapping tuple for lines indicated by
    line marks inside pyasm_lines. These are line that start with
       ^\s+\d+:
    For example:
        0:           0 |97 00| RESUME               0
        4:           2 |64 00| LOAD_CONST           ("a") ; TOS = "a"
    ^^^^^

    """
    from_to_pairs = []
    for i, line in enumerate(pyasm_lines):
        match = re.match(r"^\s+(\d+):", line)
        if match:
            from_to_pairs.append((int(match.group(1)), i))

    return tuple(from_to_pairs)
