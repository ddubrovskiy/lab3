import pytest
from calculator.evaluator import Evaluator
from calculator.exceptions import CalculationError

def test_evaluation():
    evaluator = Evaluator()
    assert evaluator.evaluate({'op': '+', 'left': {'value': 2}, 'right': {'value': 3}}) == 5
    assert evaluator.evaluate({'op': '/', 'left': {'value': 10}, 'right': {'value': 2}}) == 5

def test_errors():
    evaluator = Evaluator()
    with pytest.raises(CalculationError):
        evaluator.evaluate({'op': '/', 'left': {'value': 1}, 'right': {'value': 0}})