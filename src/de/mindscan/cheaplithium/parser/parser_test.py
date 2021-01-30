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
from de.mindscan.cheaplithium.parser.ast import Literal, Env, This, VMPrimary, VMApply, VMAssignment, VMBody,\
    VMLithiumCompileUnit


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
        
    def testParseLLLiteral_EmptyStringDQ_expectEmptyStringWithoutDQ(self):
        # arrange
        parser = self.parserHelper('""')
        
        # act
        result = parser.parseLLLiteral()
        
        # assert
        self.assertEqualAST(result, Literal(value=""))
        

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

    def testParseLLMethodInvocation_InvokeTransitionsIsEqualTwoArguments_expectVMApplyNodeWithTwoArguments(self):
        # arrange
        parser = self.parserHelper('transitions.isEqual(True, False)')
        
        # act
        result = parser.parseLLMethodInvocation()
        
        # assert
        transitions = Literal(value="transitions")
        istrue = Literal(value="isEqual")
        transitions_istrue = VMPrimary(value=transitions, selector=istrue)
        booleantrue = Literal(value="True")
        booleanfalse = Literal(value="False")
        self.assertEqualAST(result, VMApply(func=transitions_istrue, arguments = [booleantrue, booleanfalse]) )

    def textParseLLAssignment_expectSomething(self):
        # arrange
        parser = self.parserHelper('x = common.add(1,2)')
        
        # act
        result = parser.parseLLAssignment()
        
        # assert
        left = Literal(value="x")
        common = Literal(value="common")
        add = Literal(value="add")
        common_add = VMPrimary(value=common, selector=add)
        one = Literal(value = 1)
        two = Literal(value = 2)
        common_add_invoke = VMApply(func = common_add, argments=[one, two])
        self.assertEqualAST(result, VMAssignment(left=left, right=common_add_invoke ))
        
    def textParseLLExpressionStatement_expectSomething(self):
        # arrange
        parser = self.parserHelper('x = common.add(1,2)')
        
        # act
        result = parser.parseLLExpressionStatement()
        
        # assert
        left = Literal(value="x")
        common = Literal(value="common")
        add = Literal(value="add")
        common_add = VMPrimary(value=common, selector=add)
        one = Literal(value = 1)
        two = Literal(value = 2)
        common_add_invoke = VMApply(func = common_add, argments=[one, two])
        self.assertEqualAST(result, VMAssignment(left=left, right=common_add_invoke ))
        
    def testParseLLExpressionStatement_InvokeTransitionsIsEqualTwoArguments_expectVMApplyNodeWithTwoArguments(self):
        # arrange
        parser = self.parserHelper('transitions.isEqual(True, False)')
        
        # act
        result = parser.parseLLExpressionStatement()
        
        # assert
        transitions = Literal(value="transitions")
        istrue = Literal(value="isEqual")
        transitions_istrue = VMPrimary(value=transitions, selector=istrue)
        booleantrue = Literal(value="True")
        booleanfalse = Literal(value="False")
        self.assertEqualAST(result, VMApply(func=transitions_istrue, arguments = [booleantrue, booleanfalse]) )
    
    def testParseLLStatement_AssignYToX_expectAnAssignment(self):
        # arrange
        parser = self.parserHelper('x=y;')
        
        # act
        result = parser.parseLLStatement()
        
        # assert
        x = Literal(value="x")
        y = Literal(value="y")
        self.assertEqualAST(result, VMAssignment(left=x, right=y) )

    def testParseLLStatement_AssignYInvocationToX_expectAnAssignmentNode(self):
        # arrange
        parser = self.parserHelper('x=y();')
        
        # act
        result = parser.parseLLStatement()
        
        # assert
        x = Literal(value="x")
        y = Literal(value="y")
        y_invoke = VMApply(func = y, arguments=[])

        self.assertEqualAST(result, VMAssignment(left=x, right=y_invoke) )
        
    def testParseLLStatement_YInvocation_expectAnInvocationNode(self):
        # arrange
        parser = self.parserHelper('y();')
        
        # act
        result = parser.parseLLStatement()
        
        # assert
        y = Literal(value="y")

        self.assertEqualAST(result, VMApply(func = y, arguments=[]) )
        
    def testParseVMBody_EmptyBody_expectVMBodyWithEmptyStatementsArray(self):
        # arrange
        parser = self.parserHelper('{}')
        
        # act
        result = parser.parseVMBody()
        
        # assert
        self.assertEqualAST(result, VMBody(statements=[]) )

#     def testParseVMBody_prematureBody_expectVMBodyWithEmptyStatementsArray(self):
#         # arrange
#         parser = self.parserHelper('{')
#         
#         # act
#         result = parser.parseVMBody()
#         
#         # assert
#         self.assertEqualAST(result, VMBody(statements=[]) )

    def testParseVMBody_SingleAssignment_expectVMBodyWithAssignmentStatement(self):
        # arrange
        parser = self.parserHelper('{ a=b; }')
        
        # act
        result = parser.parseVMBody()
        
        # assert
        a = Literal(value = 'a')
        b = Literal(value = 'b')
        assign_b_to_a = VMAssignment(left = a, right = b)
        self.assertEqualAST(result, VMBody(statements=[assign_b_to_a]) )
        
    def testParseVMBody_TwoAssignments_expectVMBodyWithTwoAssignmentStatements(self):
        # arrange
        parser = self.parserHelper('{ a=b; a=b;}')
        
        # act
        result = parser.parseVMBody()
        
        # assert
        a = Literal(value = 'a')
        b = Literal(value = 'b')
        assign_b_to_a = VMAssignment(left = a, right = b)
        self.assertEqualAST(result, VMBody(statements=[assign_b_to_a, assign_b_to_a]) )
        

    def testParseVMBody_SingleInvocation_expectVMBodyWithInvokeStatement(self):
        # arrange
        parser = self.parserHelper('{ a(); }')
        
        # act
        result = parser.parseVMBody()
        
        # assert
        a = Literal(value = 'a')
        invoke_a = VMApply(func = a, arguments=[] )
        self.assertEqualAST(result, VMBody(statements=[invoke_a]) )

    def testParseVMBody_TwoInvocations_expectVMBodyWithTwoInvokeStatements(self):
        # arrange
        parser = self.parserHelper('{ a(); a(); }')
        
        # act
        result = parser.parseVMBody()
        
        # assert
        a = Literal(value = 'a')
        invoke_a = VMApply(func = a, arguments=[] )
        self.assertEqualAST(result, VMBody(statements=[invoke_a, invoke_a]) )
    
    def testParseVMLithiumCompileUnit_EmptyBody_returnsEmptyVMCompileUnit(self):
        # arrange
        parser = self.parserHelper('')
        
        # act
        result = parser.parseVMLithiumCompileUnit()
        
        # assert
        self.assertEqualAST(result, VMLithiumCompileUnit() )
        
    def testParseVMLithiumCompileUnit_transitionAlwaysNoBody_returnsVMCompileUnitWithInvocationInGuard(self):
        # arrange
        parser = self.parserHelper('transitions.always()')
        
        # act
        result = parser.parseVMLithiumCompileUnit()
        
        # assert
        transitions=Literal(value="transitions")
        always = Literal(value="always")
        transitions_always = VMPrimary(value = transitions, selector=always)
        guard = VMApply(func=transitions_always, arguments=[])
        self.assertEqualAST(result, VMLithiumCompileUnit(guard = guard) )
        
    def testParseVMLithiumCompileUnit_transitionAlwaysEmptyBody_returnsVMCompileUnitWithInvocationInGuardAndEmptyBody(self):
        # arrange
        parser = self.parserHelper('transitions.always() {}')
        
        # act
        result = parser.parseVMLithiumCompileUnit()
        
        # assert
        transitions=Literal(value="transitions")
        always = Literal(value="always")
        transitions_always = VMPrimary(value = transitions, selector=always)
        guard = VMApply(func=transitions_always, arguments=[])
        empty_body = VMBody(statements=[])
        self.assertEqualAST(result, VMLithiumCompileUnit(guard = guard,body=empty_body) )
    


    def assertEqualAST(self, result, expected):
        self.assertEqual(str(result), str(expected))
        
    def parserHelper(self, code) -> LithiumParser:
        tokens = tokenizer.tokenize(code)
        
        return LithiumParser(tokens)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()