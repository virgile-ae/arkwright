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

    def test_assignment(self):
        expected = 'let foo = "hello";'
        inpt = '(let foo "hello")'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)

    def test_list(self):
        expected = '[123.0, -12.2, "hello", true, false, null]'
        inpt = '[123 -12.2 "hello" true false nil]'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)

    def test_function(self):
        expected = 'function hello() {\n  return "hello"\n}'
        inpt = '(func hello [] "hello")'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)

    def test_index(self):
        expected = '[1.0, 2.0, 3.0, 4.0].at(0.0)'
        inpt = '(nth [1 2 3 4] 0)'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)

    def test_do_statement(self):
        expected = '(() => { \n  return console.log("hi")\n})()'
        inpt = '(do (print "hi"))'
        result = compilation.compile_to_js(inpt)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
