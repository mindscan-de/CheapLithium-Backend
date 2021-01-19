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

from types import ModuleType

from . import interpreter
from de.mindscan.cheaplithium.parser.ast import Literal, Env, DictSelector, VMModule, VMPrimary, VMApply, VMLithiumCompileUnit

# TODO: work on the execution model first

class Test(unittest.TestCase):

    def testEvalTransition_invokeTransitionsAlways_expectReturnsTrue(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='always'))
        vmprimary = VMPrimary(value = module, selector = selector)
        guard = VMApply(func=vmprimary, arguments=[])
        compileunit = VMLithiumCompileUnit(guard=guard, body = None)
        # act
        result = interpreter.eval_transition(compileunit,{})  
        # assert
        self.assertEquals(result, True)


    def testEvalTransition_invokeTransitionsNever_expectReturnsFalse(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='never'))
        vmprimary = VMPrimary(value = module, selector = selector)
        guard = VMApply(func=vmprimary, arguments=[])
        compileunit = VMLithiumCompileUnit(guard=guard, body = None)
        # act
        result = interpreter.eval_transition(compileunit,{})  
        # assert
        self.assertEquals(result, False)


    def testEvalTransition_invokeTransitionsIsTrue_expectReturnsTrue(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='isTrue'))
        vmprimary = VMPrimary(value = module, selector = selector)
        guard = VMApply(func=vmprimary, arguments=[Literal(value=True)])
        compileunit = VMLithiumCompileUnit(guard=guard, body = None)
        # act
        result = interpreter.eval_transition(compileunit,{})  
        # assert
        self.assertEquals(result, True)


    def testEvalTransition_invokeTransitionsIsTrueWithFalse_expectReturnsFalse(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='isTrue'))
        vmprimary = VMPrimary(value = module, selector = selector)
        guard = VMApply(func=vmprimary, arguments=[Literal(value=False)])
        compileunit = VMLithiumCompileUnit(guard=guard, body = None)
        # act
        result = interpreter.eval_transition(compileunit,{})  
        # assert
        self.assertEquals(result, False)


        
    
    def testEvalLL_invokeEnv_expectReturnsEnvironment(self):
        environment = {'this':'is the environment'}
        ast = Env()
        result = interpreter.eval_ll(ast, environment)
        self.assertDictEqual(result, environment)
        
    def testEvalLL_invokeEnvWithSelector_expectReturnsEnvironmentValue(self):
        environment = {'this':'is the environment'}
        ast = Env(selector=DictSelector(index=Literal(value='this')))
        result = interpreter.eval_ll(ast, environment)
        self.assertEqual(result, 'is the environment')
        
    def testEvalLL_invokeEnvWithSelectorOtherKey_expectReturnsOthertValue(self):
        environment = {'this':'is the environment','otherKey':'otherValue'}
        ast = Env(selector=DictSelector(index=Literal(value='otherKey')))
        result = interpreter.eval_ll(ast, environment)
        self.assertEqual(result, 'otherValue')
    
    def testEvalLL_invokeVMModuleForTransitions_expectResultIsModuleType(self):
        ast = VMModule(name=Literal(value='transitions'))
        result = interpreter.eval_ll(ast, {})
        self.assertIsInstance(result, ModuleType)
        
    def testEvalLL_invokeVMModuleForTransitions_expectModuleNameIsTransitions(self):
        ast = VMModule(name=Literal(value='transitions'))
        result = interpreter.eval_ll(ast, {})
        self.assertEquals(result.__name__, 'de.mindscan.cheaplithium.vm.transitions')
        
        
    def testEvalLL_selectVMModuleAlwaysMethod_expectMethodNameIsAlways(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='always'))
        ast = VMPrimary(value = module, selector = selector)
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result.__name__, "always")
        
    def testEvalLL_invokeVMModuleAlwaysMethod_expectMethodResultIsTrue(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='always'))
        vmprimary = VMPrimary(value = module, selector = selector)
        ast = VMApply(func=vmprimary, arguments=[])
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result, True)

    def testEvalLL_invokeVMModuleNeverMethod_expectMethodResultIsFalse(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='never'))
        vmprimary = VMPrimary(value=module, selector = selector)
        ast = VMApply(func = vmprimary, arguments=[])
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result, False)

    def testEvalLL_invokeVMModuleIsTrueMethodWithTrueValue_expectMethodResultIsTrue(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='isTrue'))
        vmprimary = VMPrimary(value=module, selector = selector)
        ast = VMApply(func = vmprimary, arguments=[Literal(value=True)])
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result, True)
        
    def testEvalLL_invokeVMModuleIsTrueMethodWithFalseValue_expectMethodResultIsFalse(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='isTrue'))
        vmprimary = VMPrimary(value=module, selector = selector)
        ast = VMApply(func = vmprimary, arguments=[Literal(value=False)])
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result, False)

    def testEvalLL_invokeVMModuleIsLessThanMethod1020_expectMethodResultIsTrue(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='isLessThan'))
        vmprimary = VMPrimary(value=module, selector = selector)
        ast = VMApply(func = vmprimary, arguments=[Literal(value=10), Literal(value=20)])
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result, True)

    def testEvalLL_invokeVMModuleIsLessThanMethod2010_expectMethodResultIsFalse(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='isLessThan'))
        vmprimary = VMPrimary(value=module, selector = selector)
        ast = VMApply(func = vmprimary, arguments=[Literal(value=20), Literal(value=10)])
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result, False)

    def testEvalLL_invokeIsTrueWithEnvValueTrue_expectReturnsTrue(self):
        # arrange
        environment = {'myValue':True}
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='isTrue'))
        vmprimary = VMPrimary(value=module, selector = selector)
        ast = VMApply(func = vmprimary, arguments=[Env(selector=DictSelector(index=Literal(value='myValue')))])
        # act
        result = interpreter.eval_ll(ast, environment)
        # assert
        self.assertEquals(result, True)

    def testEvalLL_invokeIsTrueWithEnvValueFalse_expectReturnsFalse(self):
        # arrange
        environment = {'myValue':False}
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='isTrue'))
        vmprimary = VMPrimary(value=module, selector = selector)
        ast = VMApply(func = vmprimary, arguments=[Env(selector=DictSelector(index=Literal(value='myValue')))])
        # act
        result = interpreter.eval_ll(ast, environment)
        # assert
        self.assertEquals(result, False)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()