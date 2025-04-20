import pytest
from calculator.parser import Parser
from calculator.exceptions import InvalidExpressionError

def test_scientific_notation():
    parser = Parser()
    assert parser.parse("1.25e+3") == {'value': 1250.0}

def test_power_operator():
    parser = Parser()
    assert parser.parse("2^3") == {'op': '^', 'left': {'value': 2}, 'right': {'value': 3}}

def test_brackets():
    parser = Parser()
    assert parser.parse("(2+3)*4") == {
        'op': '*',
        'left': {
            'op': '+',
            'left': {'value': 2},
            'right': {'value': 3}
        },
        'right': {'value': 4}
    }