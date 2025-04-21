import pytest
import math
from calculator.parser import Parser
from calculator.evaluator import Evaluator

def test_functions():
    parser = Parser()
    
    assert math.isclose(Evaluator().evaluate(parser.parse("pi")), math.pi)
    assert math.isclose(Evaluator().evaluate(parser.parse("e")), math.e)

    evaluator = Evaluator()
    assert math.isclose(evaluator.evaluate(parser.parse("sqrt(4)")), 2.0)
    assert math.isclose(evaluator.evaluate(parser.parse("sin(pi/2)")), 1.0)
    assert math.isclose(evaluator.evaluate(parser.parse("ln(e^3)")), 3.0)

def test_angle_units():
    parser = Parser()
    evaluator_degree = Evaluator(angle_unit='degree')
    assert math.isclose(evaluator_degree.evaluate(parser.parse("sin(90)")), 1.0)
    assert math.isclose(evaluator_degree.evaluate(parser.parse("cos(0)")), 1.0)