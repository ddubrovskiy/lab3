from calculator.exceptions import CalculationError
import math

class Evaluator:
    def __init__(self, angle_unit='radian'):
        self.angle_unit = angle_unit  # 'radian' или 'degree'

    def evaluate(self, node: dict) -> float:
        if 'value' in node:
            return node['value']
        elif 'constant' in node:
            if node['constant'] == 'pi':
                return math.pi
            elif node['constant'] == 'e':
                return math.e
            else:
                raise CalculationError(f"Неизвестная константа: {node['constant']}")
        elif 'function' in node:
            func_name = node['function']
            arg = self.evaluate(node['argument'])
            if func_name in ('sin', 'cos', 'tg', 'ctg'):
                if self.angle_unit == 'degree':
                    arg = math.radians(arg)
            if func_name == 'sqrt':
                if arg < 0:
                    raise CalculationError("Корень из отрицательного числа")
                return math.sqrt(arg)
            elif func_name == 'sin':
                return math.sin(arg)
            elif func_name == 'cos':
                return math.cos(arg)
            elif func_name == 'tg':
                return math.tan(arg)
            elif func_name == 'ctg':
                if math.isclose(math.sin(arg), 0, abs_tol=1e-12):
                    raise CalculationError("Котангенс не определен")
                return 1 / math.tan(arg)
            elif func_name == 'ln':
                if arg <= 0:
                    raise CalculationError("Логарифм не определен")
                return math.log(arg)
            elif func_name == 'exp':
                return math.exp(arg)
            else:
                raise CalculationError(f"Неизвестная функция: {func_name}")
        elif 'op' in node:
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right'])
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
        else:
            raise CalculationError("Некорректное выражение")