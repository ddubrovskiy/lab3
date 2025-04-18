import pytest
from calculator.parser import Parser
from calculator.exceptions import InvalidExpressionError

def test_valid_expressions():
    parser = Parser()
    assert parser.parse("2+3") == {'op': '+', 'left': {'value': 2}, 'right': {'value': 3}}
    assert parser.parse("4.5*2") == {'op': '*', 'left': {'value': 4.5}, 'right': {'value': 2}}

def test_invalid_expressions():
    parser = Parser()
    with pytest.raises(InvalidExpressionError):
        parser.parse("2^3")
    with pytest.raises(InvalidExpressionError):
        parser.parse("1+")