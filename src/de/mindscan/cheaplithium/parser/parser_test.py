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
from de.mindscan.cheaplithium.parser.ast import Literal, Env, This, VMPrimary, VMApply


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
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value=True))
        
    def testParseLLLiteral_BooleanFalse_expectLiteralWithBooleanFalse(self):
        # arrange
        parser = self.parserHelper("False")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value=False))
        
    def testParseLLLiteral_IntegerZero_expectLiteralWithIntegerValueZero(self):
        # arrange
        parser = self.parserHelper("0")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value=0))

    def testParseLLLiteral_IntegerOne_expectLiteralWithIntegerValueOne(self):
        # arrange
        parser = self.parserHelper("1")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value=1))
        
        
    def testParseLLLiteral_Integer123_expectLiteralWithIntegerValue123(self):
        # arrange
        parser = self.parserHelper("123")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value=123))
        

    def testParseLLLiteral_None_expectLiteralWithValueNone(self):
        # arrange
        parser = self.parserHelper("None")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value=None))

    def testParseLLLiteral_LiteralMember1_expectLiteralWithValueMember1(self):
        # arrange
        parser = self.parserHelper("member1")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value="member1"))

    def testParseLLLiteral_LiteralMember2_expectLiteralWithValueMember2(self):
        # arrange
        parser = self.parserHelper("member2")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value="member2"))
        
    def testParseLLLiteral_LiteralX_expectLiteralWithValueX(self):
        # arrange
        parser = self.parserHelper("x")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value="x"))
        
    def testParseLLLiteral_LiteralY_expectLiteralWithValueY(self):
        # arrange
        parser = self.parserHelper("y")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value="y"))

    def testParseLLLiteral_Env_expectEnvironment(self):
        # arrange
        parser = self.parserHelper("env")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Env())
        
    def testParseLLLiteral_This_expectThis(self):
        # arrange
        parser = self.parserHelper("this")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, This())
        
    def testParseLLLiteral_StringHelloWorldSQ_expectStringHelloWorldWithoutSQ(self):
        # arrange
        parser = self.parserHelper("'HelloWorld'")
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value="HelloWorld"))
        
    def testParseLLLiteral_StringHelloWorldDQ_expectStringHelloWorldWithoutDQ(self):
        # arrange
        parser = self.parserHelper('"HelloWorld"')
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value="HelloWorld"))

    def testParseLLMemberSelection_ADotB_expectPrimaryOfLiteralUsingALiteral(self):
        # arrange
        parser = self.parserHelper('a.b')
        
        # act
        result = parser.parseLLMemberSelection()
        
        # assert
        self.assertEqualAST(result, VMPrimary(value=Literal(value='a'), selector=Literal(value='b') ) )
        
    def testParseLLMemberSelection_ADotBDotC_expectPrimaryOfLiteralUsingALiteral(self):
        # arrange
        parser = self.parserHelper('a.b.c')
        
        #act
        result = parser.parseLLMemberSelection()
        
        #assert
        a = Literal(value='a')
        b = Literal(value='b')
        a_b = VMPrimary(value=a, selector=b )
        c = Literal(value='c')
        a_b_c = VMPrimary(value=a_b, selector=c )
        self.assertEqualAST(result, a_b_c )

    def testParseLLMemberSelection_ADotBDotCDotD_expectPrimaryOfLiteralUsingALiteral(self):
        # arrange
        parser = self.parserHelper('a.b.c.d')
        
        # act
        result = parser.parseLLMemberSelection()
        
        # assert
        a = Literal(value='a')
        b = Literal(value='b')
        a_b = VMPrimary(value=a, selector=b )
        c = Literal(value='c')
        a_b_c = VMPrimary(value=a_b, selector=c )
        d = Literal(value='d')
        a_b_c_d = VMPrimary(value=a_b_c, selector=d )
        self.assertEqualAST(result, a_b_c_d )
        
    def testParseLLMethodInvocation_InvokeInvokeMe_expectVMApplyNode(self):
        # arrange
        parser = self.parserHelper('invokeMe()')
        
        # act
        result = parser.parseLLMethodInvocation()
        
        # assert
        self.assertEqualAST(result, VMApply(func=Literal(value="invokeMe"), arguments = []) )

    def testParseLLMethodInvocation_InvokeTransitionsAlways_expectVMApplyNode(self):
        # arrange
        parser = self.parserHelper('transitions.always()')
        
        # act
        result = parser.parseLLMethodInvocation()
        
        # assert
        transitions = Literal(value="transitions")
        always = Literal(value="always")
        transitions_always = VMPrimary(value=transitions, selector=always)
        self.assertEqualAST(result, VMApply(func=transitions_always, arguments = []) )

    def testParseLLMethodInvocation_InvokeTransitionsIsTrueOneArgument_expectVMApplyNodeWithOneArgument(self):
        # arrange
        parser = self.parserHelper('transitions.isTrue(True)')
        
        # act
        result = parser.parseLLMethodInvocation()
        
        # assert
        transitions = Literal(value="transitions")
        istrue = Literal(value="isTrue")
        transitions_istrue = VMPrimary(value=transitions, selector=istrue)
        booleantrue = Literal(value="True")
        self.assertEqualAST(result, VMApply(func=transitions_istrue, arguments = [booleantrue]) )


        

    def assertEqualAST(self, result, expected):
        self.assertEqual(str(result), str(expected))
        
    def parserHelper(self, code) -> LithiumParser:
        tokens = tokenizer.tokenize(code)
        
        return LithiumParser(tokens)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()