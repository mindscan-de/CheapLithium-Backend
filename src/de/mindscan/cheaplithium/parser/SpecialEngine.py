'''
Created on 20.01.2021

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


class SpecialEngine(object):
    '''
    classdocs
    '''

    def __init__(self, params=None):
        '''
        Constructor
        '''
        self._isInterfaceRenderMode = False
        self._inputInterface = []
        self._userLabelledInput = {}
        self._thisStore = {}
    
    # #########################################
    # Interface render Mode 
    # #########################################
    
    def setInterfaceRenderMode(self, renderMode):
        self._isInterfaceRenderMode = renderMode
        
    def isInterfaceRenderMode(self):
        return self._isInterfaceRenderMode
    
    # #########################################
    # User Interface Collection 
    # #########################################
    
    def appendInputInterface(self, inputInterfaceItem):
        self._inputInterface.append(inputInterfaceItem)
        
    def getInputInterface(self):
        return self._inputInterface.copy()
    
    # #########################################
    # User Input Data Injection 
    # #########################################
    
    def setUserLabeledInput(self, labelData):
        if isinstance(labelData, dict):
            self._userLabelledInput = labelData
        else:
            self._userLabelledInput = {}

    def getUserLabelledInput(self, label):
        if label in self._userLabelledInput:
            return self._userLabelledInput[label]
        else:
            return label+"Missing"
        
        
    def isModuleName(self,modulename):
        return modulename in ('transitions', 'uilib', 'stdlib', 'cmplib', 'transitlib')
    
    # #########################################
    # This storage implementation
    # #########################################
    
    def getThis(self):
        return self._thisStore
    
    def getThisByRef(self):
        return [self._thisStore]