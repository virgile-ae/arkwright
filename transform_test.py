import unittest
import compilation


class TestTransform(unittest.TestCase):

    def test_hello_world(self):
        expected = 'console.log("hello world")'
        inpt = '(print "hello world")'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(result, expected)

    def test_bin_ops(self):
        expected = '((3.0 * 2.0) + (21.0 - 2.0))'
        inpt = '(+ (* 3 2) (- 21 2))'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)

    def test_var(self):
        expected = '\nvar foo = "hello";'
        inpt = '(var foo "hello")'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)

    def test_list(self):
        expected = '[ 123.0, -12.2, "hello", true, false, null ]'
        inpt = '[123 -12.2 "hello" true false nil]'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)

    def test_function(self):
        expected = 'function hello() { return "hello" };\n'
        inpt = '(func hello [] "hello")'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)

    def test_index(self):
        expected = ' [ 1.0, 2.0, 3.0, 4.0 ][0.0]'
        inpt = '(nth [1 2 3 4] 0)'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
