import unittest

from lex import Lexeme, lex
from errors import ErrorHandler


error_handler = ErrorHandler()


class TestLexer(unittest.TestCase):

    def test_some_keywords(self):
        input_string = 'let if or nil'
        lexemes = lex(input_string, error_handler)
        expected = [
            Lexeme('keyword', 'let'),
            Lexeme('keyword', 'if'),
            Lexeme('keyword', 'or'),
            Lexeme('nil', None)
        ]
        self.assertEqual(lexemes, expected)

    def test_some_patterns(self):
        input_string = 'true "hi 123" 123.23 abra'
        lexemes = lex(input_string, error_handler)
        expected = [
            Lexeme('boolean', True),
            Lexeme('string', 'hi 123'),
            Lexeme('number', 123.23),
            Lexeme('variable', 'abra'),
        ]
        self.assertEqual(lexemes, expected)

    def test_delimiters(self):
        input_string = '( [ ] )'
        lexemes = lex(input_string, error_handler)
        expected = [
            Lexeme('left paren', '('),
            Lexeme('left bracket', '['),
            Lexeme('right bracket', ']'),
            Lexeme('right paren', ')'),
        ]
        self.assertEqual(lexemes, expected)

    def test_whitespace(self):
        input_string = '\n\n  \t\t'
        lexemes = lex(input_string, error_handler)
        expected = []
        self.assertEqual(lexemes, expected)

    def test_comment(self):
        input_string = '// some helpful comment'
        lexemes = lex(input_string, error_handler)
        expected = []
        self.assertEqual(lexemes, expected)


if __name__ == '__main__':
    unittest.main()
