from lex import Lexeme, lex
from parse import parse, parse_expression, parse_sexpr, parse_value, parse_list, Value, SExpr
import unittest
from errors import ErrorHandler

error_handler = ErrorHandler()


class TestParse(unittest.TestCase):

    def test_parse(self):
        expected = [
            SExpr('print', [Value('string', 'hello', 1)], 1),
            SExpr('map', [
                Value('variable', 'fn', 1),
                Value('list', [
                    Value('boolean', True, 1),
                    Value('boolean', False, 1),
                    Value('number', 23.0, 1),
                ], 1)
            ], 1)
        ]
        inputted = lex(
            '(print "hello") (map fn [true false 23])', error_handler)
        output = parse(inputted, error_handler)
        self.assertEqual(expected, output)

    def test_parse_failure(self):
        expected = []
        inputted = []
        output = parse(inputted, error_handler)
        self.assertEqual(expected, output)

    def test_parse_expression(self):
        expected = SExpr('let',
                         [Value('variable', 'hi', 1),
                          Value('number', 23.0, 1)], 1), []
        inputted = lex('(let hi 23)', error_handler)
        output = parse_expression(inputted)
        self.assertEqual(expected, output)

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
        expected = Value('string', 'hello', 1), []
        inputted = [Lexeme('string', 'hello')]
        output = parse_value(inputted)
        self.assertEqual(expected, output)

    def test_parse_value_failure(self):
        expected = None
        inputted = []
        output = parse_value(inputted)
        self.assertEqual(expected, output)

    def test_parse_list(self):
        expected = Value('list', [Value('number', -123.2, 1)], 1), []
        inputted = lex('[-123.2]', error_handler)
        output = parse_list(inputted)
        self.assertEqual(expected, output)

    def test_parse_list_failure(self):
        expected = None
        inputted = []
        output = parse_list(inputted)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()
