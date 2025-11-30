from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    ID = auto(),
    NUMBER = auto()
    OPERATOR = auto(),
    LPAREN = auto()
    RPAREN = auto()

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
        return f"{self.type}({self.value!r})"
