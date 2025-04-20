import re
from typing import List, Union
from calculator.exceptions import InvalidExpressionError

class Parser:
    def __init__(self):
        self.tokens = []
        self.pos = 0

    def tokenize(self, expression: str) -> List[str]:
        token_pattern = re.compile(r'''
            (\d+\.?\d*([eE][+-]?\d+)?|\.\d+([eE][+-]?\d+)?)  # Числа с научной нотацией
            |([+\-*/^()])                                     # Операторы и скобки
            |(\S)                                             # Недопустимые символы
        ''', re.VERBOSE)

        tokens = []
        for match in token_pattern.finditer(expression.replace(" ", "")):
            number, _, _, op_or_bracket, invalid = match.groups()
            if invalid:
                raise InvalidExpressionError(f"Недопустимый символ: {invalid}")
            elif number:
                tokens.append(('NUMBER', float(number)))
            elif op_or_bracket in ('+', '-', '*', '/', '^'):
                tokens.append(('OP', op_or_bracket))
            elif op_or_bracket in ('(', ')'):
                tokens.append(('BRACKET', op_or_bracket))

        print("Tokens:", tokens)
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
        if self.pos >= len(self.tokens):
            raise InvalidExpressionError("Неожиданный конец выражения")

        token_type, token_value = self.tokens[self.pos]

        # Обработка скобок
        if token_type == 'BRACKET' and token_value == '(':
            self.pos += 1
            node = self._parse_expression()  # Рекурсивный парсинг внутреннего выражения
            # Проверяем закрывающую скобку
            if self.pos >= len(self.tokens) or self.tokens[self.pos][1] != ')':
                raise InvalidExpressionError("Ожидалась закрывающая скобка ')'")
            self.pos += 1
        elif token_type == 'NUMBER':
            node = {'value': token_value}
            self.pos += 1
        else:
            raise InvalidExpressionError(f"Ожидалось число или '(', получено: {token_value}")

        # Обработка степени после скобок/чисел
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] == '^':
            op = self.tokens[self.pos][1]
            self.pos += 1
            right = self._parse_factor()
            node = {'op': op, 'left': node, 'right': right}

        return node