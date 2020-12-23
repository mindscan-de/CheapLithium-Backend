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

from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport

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

    
    def generate_thread_report(self, thread_uuid):
        thread = self.__threadProvider.select_decision_thread_by_uuid(thread_uuid)
        environment = self.__environmentProvider.select_thread_environment_by_uuid(thread[DT_ENVIRONMENT][DT_ENVIRONMENT_UUID])
        
        reported_transitions = self.build_report_items_from_environment(environment)
        
        # the result is a dictionary of 'reportitems' => [{},{}]
        # the user can then select the reportitems for the report
        reported_transitions.append({
            'nodereport':"h4. Preliminary Analysis\n\n", 
            'data':{}
            })
        reported_transitions.append({
            'nodereport':"h5. Reproduce in Simulator Environment\n\nWe could reproduce that problem using a simulated environmnt. Therefore we could investigate the context even more. ", 
            'data':{}
            })
        reported_transitions.append({
            'nodereport':"h5. Analysis of Stacktraces\n\nThe Stacktraces show a common pattern, which is related to memory allocation. Therefore the most likely cause is a memory exhaustion due to memory leaks.", 
            'data':{}
            })
        reported_transitions.append({
            'nodereport':"h5. Investigation of Leak\n\nWe could identify a pattern, when the test is executed more often. After using the Memory Analysis tool, we could identify, that the instances are not removed because they are still accessible though a HashMap. ", 
            'data':{}
            })        
        reported_transitions.append({
            'nodereport':"h5. Analysis of Rootcause\n\nBecause of the analysis, we could identify an error in the associated framework component.", 
            'data':{}})
        reported_transitions.append({
            'nodereport':"h4. Suggested Action\n\nThis problem is high risk and high effort. Since the usecase must be performed at least 1000 times or more until this issue might occur, and the normal use pattern will not invoke this scenario more than once per day, we suggest to *not fix* that issue.", 
            'data':{}})
        
        return {'reportitems' : reported_transitions}
    
    
    def build_report_items_from_environment(self, environment:dict):
        transition_report = []
        
        # collect execution report from thread_environment
        for transition in environment[DTE_TRANSITION_HISTORY]:
            node_identifier = transition[DTE_TH_ITEM_NODEIDENTIFIER]
            node_data = transition[DTE_TH_ITEM_DATA]
            node_timestamp = transition[DTE_TH_ITEM_TIMESTAMP]
            
            node, transition = self.locate_decision_node_transition(node_identifier)
            
            if transition is None:
                # TODO: 
                # that means we could not find the node any more, maybe the outcome was renamed,
                # but then we must look into the next node, which it transited into, so
                # we can then identify the transition
                # But this can be ignored/postponed until it happens and until this problem needs a solution.
                continue
            
            if node is None:
                # this node doesn't exist any more?
                # let's ignore this for now
                continue

            # TODO: now use model, report, environment(?), and thread(?) to generate a report
            # TODO: node contains node name, and probably useful signature information, which need to be transferred from runtime environment

            # create a mini report, by filling the transition template using all the other data
            mini_report = self.render_mini_report(transition[DNT_TEMPLATE], node_data)
            
            if mini_report is None:
                # if the report is rendered empty, then there is no reason to add this report item
                # the renderer can output None intentionally if template is "" or starts with something like this: "__EMPTY__" 
                continue
            
            reportitem = {
                    'nodereport': mini_report,
                    # 'modelname'
                    # 'transitionname'
                    # model uuid - for navigation in the result page?
                    # node uuid - for navigation in the result page?
                    'nodename' : node[DN_NAME],
                    'timestamp': node_timestamp,
                    'data':node_data
                }
            # currently split for reasons, will be inlined later.
            transition_report.append(reportitem)
                         
        return transition_report


    def locate_decision_node_transition(self, node_identifier):
        # load model uuid from nodeidentifier
        # load model from model_uuid using modelProvider
        # find node, by node uuid
        # find transition by index or name
        return None, None
    
    
    def render_mini_report(self, template, node_data:dict):
        return template
    
    
    