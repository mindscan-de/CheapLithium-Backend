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
import time

from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport

class DecisionThreadEnvironments(object):
    '''
    classdocs
    '''


    def __init__(self, datamodel_dir:str = ''):
        '''
        Constructor
        '''
        self.__datamodel_directory = datamodel_dir
        self.__inMemoryDatabase = {}
        
        
    def select_thread_environment_by_uuid(self, environment_uuid:str):
        if environment_uuid is None:
            return {}
        
        if environment_uuid in self.__inMemoryDatabase:
            return self.__inMemoryDatabase[environment_uuid]
        else:
            # TODO return that from disk if known, if unknown create some random environment...
            return {
                DTE_UUID : "",
                DTE_TRANSITION_HISTORY : [
                    {
                        DTE_TH_ITEM_NODEIDENTIFIER : "MODEL_UUID::NODE_UUID::TransitionNumberOrTransitioName",
                        DTE_TH_ITEM_TIMESTAMP : "",
                        DTE_TH_ITEM_DATA : {}
                        }
                    ]
                }
    
    def split_node_identifier(self, node_identifier):
        return node_identifier.split("::", maxsplit=3)
        
    def append_transition_log_entry(self, environment_uuid: str, dm_uuid:str, dn_uuid:str, outcome:str, transition_data:dict):
        environment = self.select_thread_environment_by_uuid(environment_uuid)
        
        environment[DTE_TRANSITION_HISTORY].append(
            {
                DTE_TH_ITEM_NODEIDENTIFIER:"{}::{}::{}".format(dm_uuid,dn_uuid,outcome),
                DTE_TH_ITEM_TIMESTAMP:time.time(),
                DTE_TH_ITEM_DATA:transition_data
            
            });
        
        self.__inMemoryDatabase[environment_uuid] = environment
        
        # TODO: update decision environment information on disk / serialize
        self.update_decision_environment_by_uuid(environment_uuid, environment);
        pass
    
    
    def update_decision_environment_by_uuid(self, environment_uuid:str, environment_data:dict):
        pass
        