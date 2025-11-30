from typing import Generator, Optional

from tk import Token, TokenType

LEFT_PARENTHESES = {'(', '[', '{'}
RIGHT_PARENTHESES = {')', ']', '}'}
BINOP_SYMBOLS = {'+', '-', '*', '/', '%'}


class Lexer:
    def __init__(self, data: str):
        self.data = data
        self.pos = 0

    def next(self) -> Optional[str]:
        if self.pos >= len(self.data):
            return None
        self.pos += 1
        return self.data[self.pos - 1]

    def peek(self) -> Optional[str]:
        if self.pos >= len(self.data):
            return None
        return self.data[self.pos]

    def advance(self) -> None:
        if self.pos >= len(self.data):
            raise IndexError("End of input reached")
        self.pos += 1


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


def lex_number(l: Lexer) -> Token:
    buf = ''
    while (c := l.peek()) is not None and (c.isdigit() or c == '.'):
        buf += c
        l.advance()
    return Token(TokenType.NUMBER, buf)


def lex_id(l: Lexer) -> Token:
    buf = ''
    while (c := l.peek()) is not None and c.isalnum():
        buf += c
        l.advance()
    return Token(TokenType.ID, buf)


def lex_operator(l: Lexer) -> Token:
    buf = ''
    while (c := l.peek()) is not None and c in BINOP_SYMBOLS:
        buf += c
        l.advance()
    return Token(TokenType.OPERATOR, buf)


def lex(input_str: str) -> Generator[Token]:
    l = Lexer(input_str)
    while (c := l.peek()) is not None:
        if c.strip() == '':
            l.advance()
            continue
        token_type = get_type(c)
        match token_type:
            case TokenType.NUMBER:
                yield lex_number(l)
            case TokenType.ID:
                yield lex_id(l)
            case TokenType.OPERATOR:
                yield lex_operator(l)
            case TokenType.LPAREN | TokenType.RPAREN:
                l.advance()
                yield Token(token_type, c)


def main():
    expr = 'cos(5.05%4//3)'
    tokens = list(lex(expr))
    for token in tokens:
        print(token)


if __name__ == '__main__':
    main()
