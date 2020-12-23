'''
Created on 21.12.2020

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

from de.mindscan.cheaplithium.datamodel.DecisionModel import DecisionModel
from de.mindscan.cheaplithium.datamodel.DecisionThread import DecisionThread
from de.mindscan.cheaplithium.datamodel.DecisionThreadEnvironments import DecisionThreadEnvironments
from de.mindscan.cheaplithium.datamodel.consts import DT_ENVIRONMENT, DT_ENVIRONMENT_UUID


class ThreadReportGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, decisionThreads:DecisionThread, decisionModels:DecisionModel, threadEnvironments:DecisionThreadEnvironments):
        '''
        Constructor
        '''
        self.__threadProvider = decisionThreads
        self.__modelProvider = decisionModels
        self.__environmentProvider = threadEnvironments
        

    def build_report_items_from_transitions(self):
        return []
    
    
    def generate_thread_report(self, thread_uuid):
        thread = self.__threadProvider.select_decision_thread_by_uuid(thread_uuid)
        
        environment = self.__environmentProvider.select_thread_environment_by_uuid(thread[DT_ENVIRONMENT][DT_ENVIRONMENT_UUID])
        
        # collect execution report from thread_environment
        # laod model uuid from thread
        # load model from model_uuid using modelProvider
        
        # now use model, report, environment(?), and thread(?) to generate a report
        # the result report contains a list of detailreports for each node/transition
        
        reported_transitions = self.build_report_items_from_transitions()
        
        # the result is a dictionary of 'reportitems' => [{},{}]
        # the user can then select the reportitems for the report
        reported_transitions.append({
            'template':"h4. Preliminary Analysis\n\n", 
            'data':{}
            })
        reported_transitions.append({
            'template':"h5. Reproduce in Simulator Environment\n\nWe could reproduce that problem using a simulated environmnt. Therefore we could investigate the context even more. ", 
            'data':{}
            })
        reported_transitions.append({
            'template':"h5. Analysis of Stacktraces\n\nThe Stacktraces show a common pattern, which is related to memory allocation. Therefore the most likely cause is a memory exhaustion due to memory leaks.", 
            'data':{}
            })
        reported_transitions.append({
            'template':"h5. Investigation of Leak\n\nWe could identify a pattern, when the test is executed more often. After using the Memory Analysis tool, we could identify, that the instances are not removed because they are still accessible though a HashMap. ", 
            'data':{}
            })        
        reported_transitions.append({
            'template':"h5. Analysis of Rootcause\n\nBecause of the analysis, we could identify an error in the associated framework component.", 
            'data':{}})
        reported_transitions.append({
            'template':"h4. Suggested Action\n\nThis problem is high risk and high effort. Since the usecase must be performed at least 1000 times or more until this issue might occur, and the normal use pattern will not invoke this scenario more than once per day, we suggest to *not fix* that issue.", 
            'data':{}})
        
        return {'reportitems' : reported_transitions}
    
    