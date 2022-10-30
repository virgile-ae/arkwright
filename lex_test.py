import unittest

from lex import Lexeme, lex


class TestLexer(unittest.TestCase):

    def test_some_keywords(self):
        input_string = 'var if or nil'
        lexemes = lex(input_string)
        expected = [
            Lexeme('keyword', 'var'),
            Lexeme('keyword', 'if'),
            Lexeme('keyword', 'or'),
            Lexeme('nil', None)
        ]
        self.assertEqual(lexemes, expected)

    def test_some_patterns(self):
        input_string = 'true "hi 123" 123.23 abra'
        lexemes = lex(input_string)
        expected = [
            Lexeme('boolean', True),
            Lexeme('string', 'hi 123'),
            Lexeme('number', 123.23),
            Lexeme('variable', 'abra'),
        ]
        self.assertEqual(lexemes, expected)

    def test_delimiters(self):
        input_string = '( [ ] )'
        lexemes = lex(input_string)
        expected = [
            Lexeme('left paren', '('),
            Lexeme('left bracket', '['),
            Lexeme('right bracket', ']'),
            Lexeme('right paren', ')'),
        ]
        self.assertEqual(lexemes, expected)

    def test_whitespace(self):
        input_string = '\n\n  \t\t'
        lexemes = lex(input_string)
        expected = []
        self.assertEqual(lexemes, expected)


if __name__ == '__main__':
    unittest.main()
