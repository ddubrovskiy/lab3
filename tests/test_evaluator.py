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