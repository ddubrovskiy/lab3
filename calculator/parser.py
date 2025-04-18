import re
from typing import List, Union
from calculator.exceptions import InvalidExpressionError

class Parser:
    def __init__(self):
        self.tokens = []
        self.pos = 0

    def tokenize(self, expression: str) -> List[str]:
        # Регулярное выражение для чисел (целые, дробные) и операторов
        token_pattern = re.compile(r'''
            (\d+\.?\d*|\.\d+)          # Числа: 123, 123.45, .45
            |([+\-*/])                  # Операторы
            |(\S)                       # Недопустимые символы
        ''', re.VERBOSE)

        tokens = []
        for match in token_pattern.finditer(expression.replace(" ", "")):
            number, op, invalid = match.groups()
            if invalid:
                raise InvalidExpressionError(f"Недопустимый символ: {invalid}")
            elif number:
                tokens.append(('NUMBER', float(number)))
            elif op:
                tokens.append(('OP', op))

        return tokens

    def parse(self, expression: str) -> Union[float, dict]:
        try:
            self.tokens = self.tokenize(expression)
            self.pos = 0
            return self._parse_expression()
        except Exception as e:
            raise InvalidExpressionError(str(e))

    def _parse_expression(self) -> dict:
        node = self._parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in ('+', '-'):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = {'op': op, 'left': node, 'right': self._parse_term()}
        return node

    def _parse_term(self) -> dict:
        node = self._parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in ('*', '/'):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = {'op': op, 'left': node, 'right': self._parse_factor()}
        return node

    def _parse_factor(self) -> dict:
        if self.tokens[self.pos][0] == 'NUMBER':
            value = self.tokens[self.pos][1]
            self.pos += 1
            return {'value': value}
        else:
            raise InvalidExpressionError("Ожидалось число")