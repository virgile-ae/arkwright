import unittest

from lex import Lexeme, lex


class TestLexer(unittest.TestCase):
    def test_some_keywords(self):
        input_string = 'var if or nil'
        tokens = lex(input_string)
        expected = [
            Lexeme('var', 'var'),
            Lexeme('if', 'if'),
            Lexeme('or', 'or'),
            Lexeme('nil', None)
        ]
        self.assertEqual(tokens, expected)

    def test_some_patterns(self):
        input_string = 'true "hi 123" 123.23 abra'
        tokens = lex(input_string)
        expected = [
            Lexeme('boolean', True),
            Lexeme('string', 'hi 123'),
            Lexeme('number', 123.23),
            Lexeme('identifier', 'abra'),
        ]
        self.assertEqual(tokens, expected)

    def test_whitespace(self):
        input_string = '\n\n\n   '
        tokens = lex(input_string)
        expected = []
        self.assertEqual(tokens, expected)


if __name__ == '__main__':
    unittest.main()