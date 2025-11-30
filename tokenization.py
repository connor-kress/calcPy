from enum import Enum, auto
from typing import Iterator, Optional

from binary_operator import Add, Divide, Exp, FloorDiv, Log, Multiply, Remainder, Subtract
from math_operator import MathOperator
from tk import Token
from unary_operator import Cos, Sin
from pprint import pprint


LEFT_PARENTHESES = {'(', '[', '{'}
RIGHT_PARENTHESES = {')', ']', '}'}
ALL_PARENTHESES = LEFT_PARENTHESES.union(RIGHT_PARENTHESES)


BINOP_SYMBOLS = {'+', '-', '*', '/', '%'}
BINOP_SYMBOLS_LONG = {'**', '//'}
BINOP_SYMBOLS_LONG_LENGTHS: dict[int, set[str]] = {2: {'**', '//'}}
SPECIAL_WORDS = {'log', 'cos', 'sin'}

operator_map: dict[str, type[MathOperator]] = {
    '+': Add,
    '-': Subtract,
    '*': Multiply,
    '/': Divide,
    '**': Exp,
    'log': Log,
    'cos': Cos, # unary operator
    'sin': Sin, # unary operator
    '%': Remainder,
    '//': FloorDiv,
}

class TokenType(Enum):
    WORD = auto(),
    SPECIAL_CHAR = auto(),
    PARENTHESIS = auto()
    NUMBER = auto()


def get_type(c: str) -> TokenType:
    if c.isdigit() or c == '.':
        return TokenType.NUMBER
    elif c.isalpha():
        return TokenType.WORD
    elif c in BINOP_SYMBOLS:
        return TokenType.SPECIAL_CHAR
    elif c in ALL_PARENTHESES:
        return TokenType.PARENTHESIS
    raise TypeError("Unrecognized character")


def tokenize(input_str: str) -> Iterator[Token]:
    tokens = list[tuple[Token, TokenType]]()
    if len(input_str) == 0:
        yield from ()
        return
    it = iter(input_str)
    char = next(it, None)
    buff = ''
    buff_type: Optional[TokenType] = None
    # first pass, general parsing
    while char:
        if char == ' ':
            char = next(it, None)
            continue

        char_type = get_type(char)
        if (buff != '' and
            buff_type is not None and
            (
                char_type != buff_type or
                buff_type in {TokenType.SPECIAL_CHAR, TokenType.PARENTHESIS}
            )
        ): # push & reset buff
            tokens.append((Token(buff), buff_type))
            buff, buff_type = char, char_type
        elif (buff != '' and
              buff_type is not None and
              char_type == buff_type
          ): # keep adding: number OR word
            buff += char
        elif (buff == '' and 
              buff_type is None and
              char_type is not None): # first char
            buff += char
            buff_type = char_type

        char = next(it, None)

    if buff != '' and buff_type is not None:
        tokens.append((Token(buff), buff_type))
    yield from (tk for (tk, _) in tokens)


def main():
    expr = 'cos(5.05%4//3)'
    tokens = list(tokenize(expr))
    print(tokens)


if __name__ == '__main__':
    main()
