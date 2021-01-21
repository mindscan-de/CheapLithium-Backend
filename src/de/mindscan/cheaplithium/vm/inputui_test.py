'''
Created on 21.01.2021

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

SRC_BASE_DIR  = '../../../../../src'
import sys
sys.path.insert(0,SRC_BASE_DIR)

import importlib
import unittest
from de.mindscan.cheaplithium.parser.SpecialEngine import SpecialEngine


class Test(unittest.TestCase):


    def testUserTextField_SetInputInterfaceRenderMode_resultContainsSameLabelname(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(True)
        
        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        result = theModule.user_textfield("myLabel","myDescription")
        # assert
        self.assertEqual(result['label'], 'myLabel')
        
        
    def testUserTextField_SetInputInterfaceRenderModeOtherLabelname_resultContainsTheOtherLabelname(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(True)
        
        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        result = theModule.user_textfield("myOtherLabel","myDescription")
        # assert
        self.assertEqual(result['label'], 'myOtherLabel')
        
        
    def testUserTextField_SetInputInterfaceRenderMode_resultContainsSameDescription(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(True)
        
        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        result = theModule.user_textfield("myLabel","myDescription")
        # assert
        self.assertEqual(result['description'], 'myDescription')


    def testUserTextField_SetInputInterfaceRenderModeOtherDescription_resultContainsTheOtherDescription(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(True)
        
        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        result = theModule.user_textfield("myLabel","myOtherDescription")
        # assert
        self.assertEqual(result['description'], 'myOtherDescription')
        

    def testUserTextField_SetInputInterfaceRenderMode_resultHastextfieldType(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(True)
        
        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        result = theModule.user_textfield("myLabel","myDescription")
        # assert
        self.assertEqual(result['type'], 'textfield')
        

    def testUserTextField_SetInputInterfaceRenderModeCollectInputInterface_SpecialEngineContainsFieldDescription(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(True)
        
        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        theModule.user_textfield("myLabel","myDescription")
        result = special_engine.getInputInterface()
        
        # assert
        self.assertEqual(result, [{'label':'myLabel', 'type':'textfield', 'description':'myDescription' }])

        
    def testUserTextField_NoEngineNoInputForMyLabel_expectMyLabelMissing(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(False)
        
        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        result = theModule.user_textfield("myLabel","myDescription")
        # assert
        self.assertEqual(result, 'myLabelMissing')
        
        
    def testUserTextField_NoEngineNoInputForMyOtherLabel_expectMyOtherLabelMissing(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(False)

        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        result = theModule.user_textfield("myOtherLabel","myDescription")
        
        # assert
        self.assertEqual(result, 'myOtherLabelMissing')


    def testUserTextField_SetEngineWithUserDataForMyLabel_expectMyLabelInputFromInputDictionary(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setUserLabeledInput({'myLabel':'MyLabelInput'})

        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        result = theModule.user_textfield("myLabel","myDescription")
        # assert
        self.assertEqual(result, 'MyLabelInput')


    def testUserTextArea_SetInputInterfaceRenderModeCollectInputInterface_SpecialEngineContainsFieldDescription(self):
        # arrange
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(True)
        
        theModule = self.createModule('inputui')
        theModule._inject_engine(special_engine)
        # act
        theModule.user_textarea("myLabel","myDescription")
        result = special_engine.getInputInterface()
        
        # assert
        self.assertEqual(result, [{'label':'myLabel', 'type':'textarea', 'description':'myDescription' }])



    

    def createModule(self, module_name):
        themodule = importlib.import_module('.'+module_name, package='de.mindscan.cheaplithium.vm')
        return themodule


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()