import pytest
import time
import math
from calculator.evaluator import Evaluator
from calculator.parser import Parser
from calculator.exceptions import CalculationError

def test_power():
    evaluator = Evaluator()
    assert evaluator.evaluate({'op': '^', 'left': {'value': 2}, 'right': {'value': 3}}) == 8

def test_brackets():
    evaluator = Evaluator()
    ast = {
        'op': '*',
        'left': {
            'op': '+',
            'left': {'value': 2},
            'right': {'value': 3}
        },
        'right': {'value': 4}
    }
    assert evaluator.evaluate(ast) == 20
    
def test_overload():
    expression = "1+"*249 + "1"
    
    parser = Parser()
    evaluator = Evaluator()
    
    start = time.perf_counter()
    ast = parser.parse(expression)
    result = evaluator.evaluate(ast)
    end = time.perf_counter()
    
    execution_time = end - start
    
    assert result == 250, "Получено {result}, ожидалось 250"
    assert execution_time  < 0.2, f"Время {execution_time}, предел 200мс"
     
     
def test_performance_power_chain():
    expression = "2^2^2^2"  # 2^(2^(2^2)) = 2^16 = 65536
    ast = Parser().parse(expression)
    result = Evaluator().evaluate(ast)
    assert math.isclose(result, 65536.0)
    
def test_performance_scientific_notation():
    expression = "1e300 * 1e300 / 1e200"  # 1e400
    ast = Parser().parse(expression)
    result = Evaluator().evaluate(ast)
    assert math.isclose(result, 1e400)
 
def test_performance_deep_brackets():
    expression = "(((((...((1 + 1)...))))))"  # 100 уровней вложенности
    brackets = "(" * 100 + "1 + 1" + ")" * 100
    ast = Parser().parse(brackets)
    result = Evaluator().evaluate(ast)
    assert math.isclose(result, 2.0)
    
def test_performance_mixed_operations():
    expression = "sqrt(2^2 + 3*4 - ln(e^5)) / 2"  # sqrt(4 + 12 - 5)/2 = sqrt(11)/2 ≈ 1.658
    ast = Parser().parse(expression)
    result = Evaluator().evaluate(ast)
    assert math.isclose(result, math.sqrt(11) / 2, rel_tol=1e-9)
    
def test_performance_long_noisy_expression():
    expression = "1 + 2 * 3 - 4 / 5 + sqrt(6) - ln(7) + 8^9 + " * 50 + "1" # 50 повторов
    ast = Parser().parse(expression)
    result = Evaluator().evaluate(ast)
    
def test_large_floating_point_numbers():
    """Тест 1: Обработка очень больших чисел с плавающей точкой"""
    parser = Parser()
    evaluator = Evaluator()
    expression = "1.23456789e300 * 9.87654321e200 / 1e100"
    expected = 1.23456789e300 * 9.87654321e200 / 1e100
    
    ast = parser.parse(expression)
    result = evaluator.evaluate(ast)
    
    assert math.isclose(result, expected, rel_tol=1e-9), f"Ожидалось {expected}, получено {result}"
    
def test_deep_function_nesting():
    """Тест 3: Глубокая вложенность функций"""
    parser = Parser()
    evaluator = Evaluator()
    expression = "sqrt(sin(cos(sin(cos(ln(e^pi))))))"
    ast = parser.parse(expression)
    result = evaluator.evaluate(ast)
    
    assert not math.isnan(result), "Результат не должен быть NaN"
    assert not math.isinf(result), "Результат не должен быть бесконечностью"
    
def test_long_expression_chain():
    """Тест 5: Длинная строка с повторяющимися операциями"""
    parser = Parser()
    evaluator = Evaluator()
    base_expr = "1.5 * 2 - 3 / 4 + sqrt(5)^2 +"
    expression = base_expr * 100 + "1"
    ast = parser.parse(expression)
    result = evaluator.evaluate(ast)
    
    assert math.isclose(result, 726.0, rel_tol=1e-3), f"Ожидалось ~725.0, получено {result}"
    
def test_operator_precedence():
    """Тест 2: Проверка приоритета операций"""
    parser = Parser()
    evaluator = Evaluator()
    expression = "10 - 3 * 2^3 / 4 + 5"  # 10 - (24/4) + 5 = 9
    ast = parser.parse(expression)
    result = evaluator.evaluate(ast)
    
    assert math.isclose(result, 9.0, rel_tol=1e-9), f"Ожидалось 9.0, получено {result}"
    
def test_extreme_subtraction():
    expression = "1000000" + " - 0.1" * 100  # 1000000 - 0.1*100 = 999900.0
    parser = Parser()
    evaluator = Evaluator()
    ast = parser.parse(expression)
    result = evaluator.evaluate(ast)
    assert math.isclose(result, 999990.0, rel_tol=1e-9)

def test_repeated_division():
    expression = "1000" + " / 2" * 10
    parser = Parser()
    evaluator = Evaluator()
    ast = parser.parse(expression)
    result = evaluator.evaluate(ast)
    assert math.isclose(result, 1000 / (2**10), rel_tol=1e-9)