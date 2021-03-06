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
import re

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
        
        return {'reportitems' : reported_transitions}
    
    
    def build_report_items_from_environment(self, environment:dict):
        transition_report = []
        
        # collect execution report from thread_environment
        for transition in environment[DTE_TRANSITION_HISTORY]:
            node_identifier = transition[DTE_TH_ITEM_NODEIDENTIFIER]
            node_data = transition[DTE_TH_ITEM_DATA]
            node_timestamp = transition[DTE_TH_ITEM_TIMESTAMP]
            
            model, node, transition = self.locate_decision_node_transition(node_identifier)
            
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
            
            if not mini_report:
                # if the report is rendered empty, then there is no reason to add this report item
                # the renderer can output None intentionally if template is "" or starts with something like this: "__EMPTY__" 
                continue
            
            reportitem = {
                    'nodereport': mini_report,
                    'modelname': model[DM_NAME],
                    'modeluuid': model[DM_UUID],
                    'transitionname': transition[DNT_NAME],
                    'nodename' : node[DN_NAME],
                    'nodeuuid' : node[DN_UUID],
                    'timestamp': node_timestamp,
                    'data':node_data
                }
            # currently split for reasons, will be inlined later.
            transition_report.append(reportitem)
                         
        return transition_report

    def locate_decision_node_transition(self, node_identifier):
        dm_uuid, dn_uuid, transition_name = self.__environmentProvider.split_node_identifier(node_identifier)
        
        # load model from model_uuid using modelProvider
        model = self.__modelProvider.select_decision_model_by_uuid(dm_uuid);
        
        # TODO: temporary, until data is fixed.
        if model is None:
            return None, None, None
        
        
        # find node, by node uuid
        node = self.__modelProvider.select_decision_node_from_decision_model(model, dn_uuid)
        
        transition = self.__modelProvider.select_transition_from_node(node, transition_name)
        
        
        return model, node, transition
    
    
    def render_mini_report(self, template, node_data:dict):
        def this_replace(match):
            varname = match.group(1)
            if varname in node_data: 
                return str(node_data[varname])
            return match

        replaced_template = re.sub(r'\{\{\{this\.(.*)\}\}\}', this_replace, template)
        return replaced_template
    
    
    