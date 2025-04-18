import sys
from calculator.parser import Parser
from calculator.evaluator import Evaluator
from calculator.exceptions import InvalidExpressionError, CalculationError

def main():
    if len(sys.argv) != 2:
        print("Использование: python main.py <выражение>")
        sys.exit(1)

    expression = sys.argv[1]
    parser = Parser()
    evaluator = Evaluator()

    try:
        ast = parser.parse(expression)
        result = evaluator.evaluate(ast)
        print(result)
        sys.exit(0)
    except (InvalidExpressionError, CalculationError) as e:
        print(f"Ошибка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()