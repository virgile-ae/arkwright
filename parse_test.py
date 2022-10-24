from lex import Lexeme
from parse import parse, parse_expression, parse_sexpr, parse_value, parse_list, SExpr, Value
import unittest

# TODO: finish writing tests

class TestParse(unittest.TestCase):
    def test_parse(self):
        pass

    def test_parse_failure(self):
        expected = []
        inputted = []
        output = parse(inputted)
        self.assertEqual(expected, output)

    def test_parse_expression(self):
        pass

    def test_parse_expression_failure(self):
        expected = None
        inputted = []
        output = parse_expression(inputted)
        self.assertEqual(expected, output)

    def test_parse_sexpr(self):
        pass

    def test_parse_sexpr_failure(self):
        expected = None
        inputted = []
        output = parse_sexpr(inputted)
        self.assertEqual(expected, output)

    def test_parse_value(self):
        expected = Value('string', 'hello'), []
        inputted = [Lexeme('string', 'hello')]
        output = parse_value(inputted)
        self.assertEqual(expected, output)

    def test_parse_value_failure(self):
        expected = None
        inputted = []
        output = parse_value(inputted)
        self.assertEqual(expected, output)

    def test_parse_list(self):
        expected = Value('list', [Value('number', -123.2)]), []
        inputted = [Lexeme('left bracket', '['), Lexeme('number', -123.2), Lexeme('right bracket', ']')]
        output = parse_list(inputted)
        self.assertEqual(expected, output)

    def test_parse_list_failure(self):
        expected = None
        inputted = [Lexeme('right bracket')]
        output = parse_list(inputted)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()