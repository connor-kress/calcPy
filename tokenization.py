from typing import Generator, Optional

from binary_operator import (
    Add,
    Divide,
    Exp,
    FloorDiv,
    Log,
    Multiply,
    Remainder,
    Subtract,
)
from tk import Token, TokenType
from unary_operator import Cos, Sin


LEFT_PARENTHESES = {'(', '[', '{'}
RIGHT_PARENTHESES = {')', ']', '}'}
ALL_PARENTHESES = LEFT_PARENTHESES.union(RIGHT_PARENTHESES)

BINOP_SYMBOLS = {'+', '-', '*', '/', '%'}
BINOP_SYMBOLS_LONG = {'**', '//'}
BINOP_SYMBOLS_LONG_LENGTHS: dict[int, set[str]] = {2: {'**', '//'}}
SPECIAL_WORDS = {'log', 'cos', 'sin'}

OPERATOR_MAP = {
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

def get_type(c: str) -> TokenType:
    if c.isdigit() or c == '.':
        return TokenType.NUMBER
    elif c.isalpha():
        return TokenType.ID
    elif c in BINOP_SYMBOLS:
        return TokenType.OPERATOR
    elif c in LEFT_PARENTHESES:
        return TokenType.LPAREN
    elif c in RIGHT_PARENTHESES:
        return TokenType.RPAREN
    else:
        raise TypeError("Unrecognized character")


def tokenize(input_str: str) -> Generator[Token]:
    tokens = list[Token]()
    if len(input_str) == 0:
        yield from ()
        return
    it = iter(input_str)
    char = next(it, None)
    buff = ''
    buff_type: Optional[TokenType] = None
    # first pass, general parsing
    while char is not None:
        if char.strip() == '':
            char = next(it, None)
            continue

        char_type = get_type(char)
        if (buff != ''
            and buff_type is not None
            and (char_type != buff_type
                 or buff_type in {TokenType.OPERATOR,
                                  TokenType.LPAREN,
                                  TokenType.RPAREN}
            )
        ): # push & reset buff
            tokens.append(Token(buff_type, buff))
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
        tokens.append(Token(buff_type, buff))
    yield from tokens


def main():
    expr = 'cos(5.05%4//3)'
    tokens = list(tokenize(expr))
    for token in tokens:
        print(token)


if __name__ == '__main__':
    main()
