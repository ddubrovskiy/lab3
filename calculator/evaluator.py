from calculator.exceptions import CalculationError
import math

class Evaluator:
    def evaluate(self, node: dict) -> float:
        try:
            if 'value' in node:
                return node['value']
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right']) if 'right' in node else None
            op = node['op']
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise CalculationError("Деление на ноль")
                return left / right
            elif op == '^':
                result = left ** right
                if math.isinf(result):
                    raise CalculationError("Арифметическое переполнение")
                return result
            else:
                raise CalculationError(f"Неизвестная операция: {op}")
        except OverflowError:
            raise CalculationError("Арифметическое переполнение")