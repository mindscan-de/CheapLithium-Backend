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
        
    
    ##
    ## Starts a new decision thread. There is no testing for any privileges, whether a model may be instantiated. 
    ##
    ## @thread_uuid if provided, the model will be instantiated within a thread, otherwise a new thread is created.
    ## for the start we only have one thread, which contains one running model. For each model run, a new thread is
    ## started.
    ## ( thread_uuid:str=None ) currently omitted 
    ##
    ##
    ##
    ##
    def start_decision_thread_by_model_uuid(self, dmuuid:str, ticketreference:str=''):
        model = self.__decisionModels.select_decision_model_by_uuid(dmuuid)
        
        if model is None:
            return None
        
        # TODO: read default environment from model, and unserialize it
        # TODO: read special environment
        # TODO: identify data to be filled out, combine model
        # TODO: if error while model runtime data calculation, return without creating a thread
        
        # TODO: merge the defaultenvironment and the individual thread environment, special data wins
        
        # TODO: insert thread,
        #   TODO: RUNTIME_ENVIRONMENT : the environment....
        #   RUNTIMESTATE : STARTED
        #   CURRENTMODELID : DMUUID
        #   STATEID : model.startNodeUUID
        
        thread_uuid = self.__decisionThreads.create_decision_thread_internal(dmuuid, model[DM_STARTNODE], ticketreference)
        
        return thread_uuid

    # ended according to the plan (e.g. end-node reached)
    def stop_decision_thread(self, thread_uuid):
        # is such process?
        # get thread information
        # set state to RT_STATE_STOPPED
        # update the thread information
        pass

    # ended not to the plan (e.g. was terminated by someone
    def terminate_decision_thread(self, thread_uuid):
        # save thread to disk / archive
        # delete from current database after archiving it
        pass
    
    ## TODO: get list of archived Threads?
    ## TODO: read information of archived Thread?
    
    # Process the special cases, the HIT provides extra human calculated data to the thread
    # HIT Human Itelligent Task
    def process_HIT(self, thread_uuid):
        pass
    
    # Process the specuak cases, the SYNC needs extra data for thre thread
    # SYNC - Synchronization Node, e.g. multiple HIT decisions requried, before it can continue 
    def process_SYNC(self, thread_uuid):
        pass
    
    # 
    def process_single_decision_thread(self, thread_uuid):
        # calls process_single_decision_node to process nodes one by one
        pass
     
    def process_single_decision_node(self, thread_uuid):
        # START
        # HIT, 
        # MIT, 
        # SYNC, 
        # END
        pass
     
    # evaluated one decision node calculation 
    def evaluate_decision_node_method(self):
        pass

    # evaluates one transition, and tells whether this applies... / First True wins
    def evaluate_decision_node_transition_method(self):
        pass
    
    # TODO: do the signature splitting and such?
    # or get from a json array? instead of parsing signatures and stuff...
    # have transition signatures
    # have node sinatures
    
    ## TODO: also provide information on functions which are callable from the decision model
    