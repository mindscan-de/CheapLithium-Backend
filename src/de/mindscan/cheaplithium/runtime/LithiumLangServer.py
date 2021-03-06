'''
Created on 12.01.2021

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
from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport

from de.mindscan.cheaplithium.datamodel.DecisionThread import DecisionThread
from de.mindscan.cheaplithium.datamodel.DecisionThreadEnvironments import DecisionThreadEnvironments
from de.mindscan.cheaplithium.datamodel.DecisionModel import DecisionModel
from de.mindscan.cheaplithium.parser import interpreter
from de.mindscan.cheaplithium.parser import parser

class LithiumLangServer(object):
    '''
    classdocs
    '''

    # TODO: then we need a commit method, and then processHIT is called for this thread...

    def __init__(self, threadProvider:DecisionThread, runtimeProvider:DecisionThreadEnvironments, modelProvider:DecisionModel):
        '''
        Constructor
        '''
        self.__threadProvider = threadProvider
        self.__runtimeProvider = runtimeProvider
        self.__modelProvider = modelProvider
        
    # TODO: helper / to compile and parse correctness for development purposes.
    # this will help to identify errors in the syntax and such...
    # TODO: code completion? proposals?

    
    # This will compile the user interface for the given Thread, and the current state.
    def compileCurrentInputInterfaceForThread(self, thread_uuid:str):
        thread = self.__threadProvider.select_decision_thread_by_uuid(thread_uuid)
        environment = self.__runtimeProvider.select_thread_environment_by_uuid(thread[DT_ENVIRONMENT][DT_ENVIRONMENT_UUID])
        model = self.__modelProvider.select_decision_model_by_uuid(thread[DT_CURRENTMODEL])
        node = self.__modelProvider.select_decision_node_from_decision_model(model, thread[DT_CURRENTNODE])
        return self.__compileNodeToInputInterFace(node, environment)
    
    def __compileNodeToInputInterFace(self, node, environment):
        emptyInterface = self.__compileEmptyInterface()

        if DN_NODEACTION not in node:
            # TODO: add parserError, that node action was not defined for this
            return emptyInterface

        # calculate, whether it is a HIT node 
        # (only HIT Nodes should return a user interface)
        if node[DN_TYPE] == DN_TYPE_HIT:
            compileunit = parser.parseToAst( node[DN_NODEACTION] )
            interface = interpreter.eval_hit_render_input_interface(compileunit, environment)
            return { 'uiInputInterface': interface}
        
        elif node[DN_TYPE] == DN_TYPE_START:
            return emptyInterface
        elif node[DN_TYPE] == DN_TYPE_MIT:
            return emptyInterface
        elif node[DN_TYPE] == DN_TYPE_END:
            return emptyInterface
        else:
            return emptyInterface


    def __compileEmptyInterface(self):
        return { 'uiInputInterface': [] }
    
    
    