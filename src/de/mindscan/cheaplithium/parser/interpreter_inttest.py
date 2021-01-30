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

    def testEvalTransition_isLessThan1020UsingEnvironmentWithEmptyBody_returnsTrue(self):
        # arrange
        environment = {'result':10}
        ast = self.parseToAst('transitions.isLessThan(env.result,20) {}')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, True)

    def testEvalTransition_isLessThan3020UsingEnvironmentWithEmptyBody_returnsFalse(self):
        # arrange
        environment = {'result':30}
        ast = self.parseToAst('transitions.isLessThan(env.result,20) {}')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, False)
    
    def testEvalTransition_isLessThan1020UsingEnvironmentWithdifferntDepth_returnsTrue(self):
        # arrange
        environment = {'result':10,'x':{'y':20}}
        ast = self.parseToAst('transitions.isLessThan(env.result,env.x.y) {}')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, True)
        
    def testEvalTransition_isLessThan3020UsingEnvironmentWithdifferntDepth_returnsFalse(self):
        # arrange
        environment = {'result':30,
                       'x': {
                           'y':20
                           }}
        ast = self.parseToAst('transitions.isLessThan(env.result,env.x.y) {}')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, False)

    def testEvalTransition_isEqualHelloWorld_returnsTrue(self):
        # arrange
        environment = {'result':"Hello World!"}
        ast = self.parseToAst('transitions.isEqual(env.result, "Hello World!") {}')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, True)
        
    def testEvalTransition_isEqualHelloWorldHelloUniverse_returnsFalse(self):
        # arrange
        environment = {'result':"Hello World!"}
        ast = self.parseToAst('transitions.isEqual(env.result, "Hello Universe!") {}')
        
        # act
        result = interpreter.eval_transition(ast, environment)
        
        # assert
        self.assertEquals(result, False)

    def testEvalHitRenderInputInterface_nopNoUserInput_returnsEmptyList(self):
        # arrange
        environment = {}
        ast = self.parseToAst('common.nop() {}')
        
        # act
        result = interpreter.eval_hit_render_input_interface(ast, environment)
        
        # assert
        self.assertEquals(result, [])
        
    def testEvalHitRenderInputInterface_nopYesNoUserInput_returnsYesnoElementList(self):
        # arrange
        environment = {}
        ast = self.parseToAst('common.nop() { inputui.user_yesnoselection("myLabel","myDescription"); }')
        
        # act
        result = interpreter.eval_hit_render_input_interface(ast, environment)
        
        # assert
        self.assertEquals(result, [{'label': 'myLabel', 'type': 'yesnoselection', 'description': 'myDescription'}])

    def testEvalHitRenderInputInterface_nopYesNoUserInput123_returnsYesnoElementList123(self):
        # arrange
        environment = {}
        ast = self.parseToAst('common.nop() { inputui.user_yesnoselection("myLabel123","myDescription123"); }')
        
        # act
        result = interpreter.eval_hit_render_input_interface(ast, environment)
        
        # assert
        self.assertEquals(result, [{'label': 'myLabel123', 'type': 'yesnoselection', 'description': 'myDescription123'}])

    def testEvalHitRenderInputInterface_nopTextFieldUserInput_returnsTextFieldElement(self):
        # arrange
        environment = {}
        ast = self.parseToAst('common.nop() { inputui.user_textfield("myLabel","myDescription"); }')
        
        # act
        result = interpreter.eval_hit_render_input_interface(ast, environment)
        
        # assert
        self.assertEquals(result, [{'label': 'myLabel', 'type': 'textfield', 'description': 'myDescription'}])

    def testEvalHitRenderInputInterface_nopTextFieldUserInput123_returnsTextFieldElement123(self):
        # arrange
        environment = {}
        ast = self.parseToAst('common.nop() { inputui.user_textfield("myLabel123","myDescription123"); }')
        
        # act
        result = interpreter.eval_hit_render_input_interface(ast, environment)
        
        # assert
        self.assertEquals(result, [{'label': 'myLabel123', 'type': 'textfield', 'description': 'myDescription123'}])

    def testEvalHitRenderInputInterface_nopTextAreaUserInput_returnsTextAreaElement(self):
        # arrange
        environment = {}
        ast = self.parseToAst('common.nop() { inputui.user_textarea("myLabel","myDescription"); }')
        
        # act
        result = interpreter.eval_hit_render_input_interface(ast, environment)
        
        # assert
        self.assertEquals(result, [{'label': 'myLabel', 'type': 'textarea', 'description': 'myDescription'}])

    def testEvalHitRenderInputInterface_nopTextAreaUserInput123_returnsTextAreaElement123(self):
        # arrange
        environment = {}
        ast = self.parseToAst('common.nop() { inputui.user_textarea("myLabel123","myDescription123"); }')
        
        # act
        result = interpreter.eval_hit_render_input_interface(ast, environment)
        
        # assert
        self.assertEquals(result, [{'label': 'myLabel123', 'type': 'textarea', 'description': 'myDescription123'}])

    def testEvalHitRenderInputInterface_nopdifferentInputs_returnsAllInputs(self):
        # arrange
        environment = {}
        ast = self.parseToAst('common.nop() { inputui.user_textarea("myLabelA","DescriptionA"); inputui.user_textfield("myLabelB","DescriptionB"); inputui.user_yesnoselection("myLabelC","myDescriptionC"); }')
        
        # act
        result = interpreter.eval_hit_render_input_interface(ast, environment)
        
        # assert
        self.assertEquals(result, [
            {'description': 'DescriptionA', 'label': 'myLabelA', 'type': 'textarea'},
            {'description': 'DescriptionB', 'label': 'myLabelB', 'type': 'textfield'},
            {'description': 'myDescriptionC', 'label': 'myLabelC', 'type': 'yesnoselection'}])
        
           

    def parseToAst(self, code):
        return self.parserHelper(code).parse()
    
    def parserHelper(self, code) -> LithiumParser:
        tokens = tokenizer.tokenize(code)
        return LithiumParser(tokens)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()