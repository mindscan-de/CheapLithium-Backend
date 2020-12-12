'''
Created on 12.12.2020

MIT License

Copyright (c) 2020 Maxim Gansert

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

# import the data model column names / property names
from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport
# import the data tables / access to data on a amore abstract level
from de.mindscan.cheaplithium.datamodel.DecisionModel import DecisionModel
from de.mindscan.cheaplithium.datamodel.DecisionThread import DecisionThread


class DecisionExecutionEngine(object):
    '''
    classdocs
    '''


    def __init__(self, decisionModels: DecisionModel, decisionThreads: DecisionThread):
        '''
        Constructor
        '''
        self.__decisionModels = decisionModels
        self.__decisionThreads = decisionThreads
        
     
    # This is executing MIT, START and END nodes (MIT - machine intelligent task)
    # if HIT node then suspend the thread
    def run(self, thread_uuid:str):
        pass
    
    # This is executing HIT nodes (HIT - human intelligent task)
    def run_hit(self, thread_uuid:str):
        # process the HIT
        # then continue with run?
        pass