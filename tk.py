from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    WORD = auto(),
    SPECIAL_CHAR = auto(),
    PARENTHESIS = auto()
    NUMBER = auto()

    def __repr__(self):
        return f"TokenType.{self.name}"

    def __str__(self):
        return self.name


@dataclass
class Token:
    type: TokenType
    value: str

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r})"

    def __str__(self):
        match self.type:
            case TokenType.WORD:
                return f"WORD({self.value!r})"
            case TokenType.SPECIAL_CHAR:
                return f"SPECIAL_CHAR({self.value!r})"
            case TokenType.PARENTHESIS:
                return f"PARENTHESIS({self.value!r})"
            case TokenType.NUMBER:
                return f"NUMBER({self.value!r})"
