import argparse
from calculator.parser import Parser
from calculator.evaluator import Evaluator
from calculator.exceptions import InvalidExpressionError, CalculationError

def main():
    parser = argparse.ArgumentParser(description='Калькулятор')
    parser.add_argument('expression', help='Арифметическое выражение')
    parser.add_argument('--angle-unit', choices=['degree', 'radian'], default='radian',
                        help='Единицы измерения углов (по умолчанию: радианы)')
    args = parser.parse_args()

    try:
        ast = Parser().parse(args.expression)
        result = Evaluator(angle_unit=args.angle_unit).evaluate(ast)
        print(result)
    except (InvalidExpressionError, CalculationError) as e:
        print(f"Ошибка: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()