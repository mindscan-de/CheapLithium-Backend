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
from de.mindscan.cheaplithium.parser.ast import Apply, Literal, MethodDeclaration, Env, DictSelector, VMModule,\
    VMPrimary, Apply2

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

    # test with access to environment
    def testEvalTransition_invokeIsTrueWithEnvValueTrue_expectReturnsTrue(self):
        environment = {'myValue':True}
        ast = Apply(name=Literal(value="isTrue"), arguments=[ Env(selector=DictSelector(index=Literal(value='myValue'))) ])
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', environment)
        self.assertEqual(result, True)
        
        # test with access to environment
    def testEvalTransition_invokeIsTrueWithEnvValueFalse_expectReturnsFalse(self):
        environment = {'myValue':False}
        ast = Apply(name=Literal(value="isTrue"), arguments=[ Env(selector=DictSelector(index=Literal(value='myValue'))) ])
        result = interpreter.eval_transition(ast, 'de.mindscan.cheaplithium.vm', 'transitions', environment)
        self.assertEqual(result, False)
    
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
        ast = Apply2(func=vmprimary, arguments=[])
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result, True)

    def testEvalLL_invokeVMModuleNeverMethod_expectMethodResultIsFalse(self):
        # arrange
        module = VMModule(name=Literal(value='transitions'))
        selector = DictSelector(index=Literal(value='never'))
        vmprimary = VMPrimary(value=module, selector = selector)
        ast = Apply2(func = vmprimary, arguments=[])
        # act
        result = interpreter.eval_ll(ast, {})
        # assert
        self.assertEquals(result, False)
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()