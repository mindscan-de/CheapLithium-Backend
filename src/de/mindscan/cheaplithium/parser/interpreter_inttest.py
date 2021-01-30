'''
Created on 30.01.2021

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

@autor: Maxim Gansert, Mindscan
'''

import unittest
from de.mindscan.cheaplithium.parser.parser import LithiumParser
from de.mindscan.cheaplithium.parser import tokenizer, interpreter

#
# Interpreter Integration Test - Some EndToEndTest 
#
class Test(unittest.TestCase):


    def testEvalTransition_TransitionsAlways_returnsTrue(self):
        # arrange
        environment = {}
        ast = self.parseToAst('transitions.always()')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, True)

    def testEvalTransition_TransitionsNever_returnsFalse(self):
        # arrange
        environment = {}
        ast = self.parseToAst('transitions.never()')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, False)

    def testEvalTransition_TransitionsIsTrueWithTrue_returnsTrue(self):
        # arrange
        environment = {}
        ast = self.parseToAst('transitions.isTrue(True)')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, True)

    def testEvalTransition_TransitionsIsTrueWithFalse_returnsFalse(self):
        # arrange
        environment = {}
        ast = self.parseToAst('transitions.isTrue(False)')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, False)

    def testEvalTransition_TransitionsIsFalseWithTrue_returnsFalse(self):
        # arrange
        environment = {}
        ast = self.parseToAst('transitions.isFalse(True)')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, False)

    def testEvalTransition_TransitionsIsFalseWithFalse_returnsTrue(self):
        # arrange
        environment = {}
        ast = self.parseToAst('transitions.isFalse(False)')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, True)

    def testEvalTransition_Empty_returnsFalse(self):
        # arrange
        environment = {}
        ast = self.parseToAst('')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, False)

    def testEvalTransition_isLessThan1020_returnsTrue(self):
        # arrange
        environment = {}
        ast = self.parseToAst('transitions.isLessThan(10,20)')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, True)

    def testEvalTransition_isLessThan1020WithEmptyBody_returnsTrue(self):
        # arrange
        environment = {}
        ast = self.parseToAst('transitions.isLessThan(10,20) {}')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, True)
        

    def parseToAst(self, code):
        return self.parserHelper(code).parse()
    
    def parserHelper(self, code) -> LithiumParser:
        tokens = tokenizer.tokenize(code)
        return LithiumParser(tokens)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()