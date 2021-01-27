'''
Created on 10.01.2021

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

from de.mindscan.cheaplithium.parser import tokenizer
from de.mindscan.cheaplithium.parser.parser import LithiumParser
from de.mindscan.cheaplithium.parser.ast import Literal


class Test(unittest.TestCase):


#     def testParse_TransitionsAlwaysNoArgsNoBody_expectLitiumCompileUnitWithGuard(self):
#         # arrange
#         tokens = tokenizer.tokenize("transitions.always()")
#         
#         #act
#         parsed_ast = parser.parse(tokens)
#         
#         #assert
#         self.assertEqual(str(parsed_ast), 'VMLithiumCompileUnit(guard:VMApply(func:Literal(value:transitions, selector:DictSelector(index:Literal(value:always, selector:None))), arguments:None), body:None)')
# 
# 
#     def testParseBody_TransitionsAlwaysNoARgumentsNoBody_expectTransition(self):
#         # arrange
#         tokens = tokenizer.tokenize("transitions.always()")
#         
#         #act
#         parsed_ast = LithiumParser(tokens).parse_guard()
#         
#         #assert
#         self.assertEqual(str(parsed_ast), 'VMApply(func:Literal(value:transitions, selector:DictSelector(index:Literal(value:always, selector:None))), arguments:None)')

    def testParseLLLiteral_BooleanTrue_expectLiteralWithBooleanTrue(self):
        # arrange
        parser = self.parserHelper("True")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value=True))
        
    def testParseLLLiteral_BooleanFalse_expectLiteralWithBooleanFalse(self):
        # arrange
        parser = self.parserHelper("False")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value=False))
        
    def testParseLLLiteral_IntegerZero_expectLiteralWithIntegerValueZero(self):
        # arrange
        parser = self.parserHelper("0")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value=0))

    def testParseLLLiteral_IntegerOne_expectLiteralWithIntegerValueOne(self):
        # arrange
        parser = self.parserHelper("1")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value=1))
        
        
    def testParseLLLiteral_Integer123_expectLiteralWithIntegerValue123(self):
        # arrange
        parser = self.parserHelper("123")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value=123))
        

    def testParseLLLiteral_None_expectLiteralWithValueNone(self):
        # arrange
        parser = self.parserHelper("None")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value=None))

    def testParseLLLiteral_LiteralMember1_expectLiteralWithValueMember1(self):
        # arrange
        parser = self.parserHelper("member1")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value="member1"))

    def testParseLLLiteral_LiteralMember2_expectLiteralWithValueMember2(self):
        # arrange
        parser = self.parserHelper("member2")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value="member2"))
        
    def testParseLLLiteral_LiteralX_expectLiteralWithValueX(self):
        # arrange
        parser = self.parserHelper("x")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value="x"))
        
    def testParseLLLiteral_LiteralY_expectLiteralWithValueY(self):
        # arrange
        parser = self.parserHelper("y")
        
        #act
        result = parser.parseLLLiteral()
        
        #assert
        self.assertEqualAST(result, Literal(value="y"))
        
        
    
    def assertEqualAST(self, result, expected):
        self.assertEqual(str(result), str(expected))
        
    def parserHelper(self, code) -> LithiumParser:
        tokens = tokenizer.tokenize(code)
        
        return LithiumParser(tokens)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()