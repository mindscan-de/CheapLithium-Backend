'''
Created on 14.01.2021

MIT License

Copyright (c) 2021 Maxim Gansert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@autor: Maxim Gansert
'''
import unittest

from . import interpreter
from de.mindscan.cheaplithium.parser.ast import Apply, Literal, MethodDeclaration

# TODO: work on the execution model first

class Test(unittest.TestCase):

    def testEvalTransition_invokeTransitionsAlways_expectReturnsTrue(self):
        ast = MethodDeclaration(name="always", parameters=None)
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', {})
        self.assertEqual(result, True)

    def testEvalTransition_invokeTransitionsNever_expectReturnsFalse(self):
        ast = MethodDeclaration(name="never", parameters=None)
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', {})
        self.assertEqual(result, False)

    #def testEvalTransition_invokeTransitionsIsTrue_expectReturnsTrue(self):
    #    ast = MethodDeclaration(name="isTrue", parameters=[])
    #    result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', {})
    #    self.assertEqual(result, True)


    # test with one method without arguments
    def testEvalTransition_invokeAlwaysTransition_expectReturnsTrue(self):
        ast = Apply(name=Literal(value="always"), arguments=[])
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', {})
        self.assertEqual(result, True)
    
    # test with a different method without arguments
    def testEvalTransition_invokeNeverTransition_expectReturnsFalse(self):
        ast = Apply(name=Literal(value="never"), arguments=[])
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', {})
        self.assertEqual(result, False)
    
    # test with one boolean argument
    def testEvalTransition_invokeIsTrueArgTrue_expectReturnsTrue(self):
        ast = Apply(name=Literal(value="isTrue"), arguments=[ Literal(value=True) ])
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', {})
        self.assertEqual(result, True)
    
    # test with one boolean argument - different return value
    def testEvalTransition_invokeIsTrueArgFalse_expectReturnsFalse(self):
        ast = Apply(name=Literal(value="isTrue"), arguments=[ Literal(value=False) ])
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', {})
        self.assertEqual(result, False)

    # test with two integer aguments
    def testEvalTransition_invokeIsLessArg1020_expectReturnsTrue(self):
        ast = Apply(name=Literal(value="isLessThan"), arguments=[ Literal(value=10), Literal(value=20) ])
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', {})
        self.assertEqual(result, True)

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()