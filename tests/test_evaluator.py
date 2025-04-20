import pytest
from calculator.evaluator import Evaluator
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