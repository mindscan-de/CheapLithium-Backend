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
from de.mindscan.cheaplithium.datamodel.DecisionThreadEnvironments import DecisionThreadEnvironments
import importlib


## TODO: work though all the other TODO tags - it will work right away I promise...

class DecisionExecutionEngine(object):
    '''
    classdocs
    '''


    def __init__(self, decisionModels: DecisionModel, decisionThreads: DecisionThread, decisionThreadEnvironments:DecisionThreadEnvironments):
        '''
        Constructor
        '''
        self.__decisionModels = decisionModels
        self.__decisionThreads = decisionThreads
        self.__decisionThreadEnvironments = decisionThreadEnvironments
        
    
    ##
    ## Starts a new decision thread. There is no testing for any privileges, whether a model may be instantiated. 
    ##
    ## @thread_uuid if provided, the model will be instantiated within a thread, otherwise a new thread is created.
    ## for the start we only have one thread, which contains one running model. For each model run, a new thread is
    ## started.
    ## ( thread_uuid:str=None ) currently omitted 
    ##
    def start_decision_thread_by_model_uuid(self, dmuuid:str, ticketreference:str=''):
        # read the model
        model = self.__decisionModels.select_decision_model_by_uuid(dmuuid)
        
        if model is None:
            return None
        
        # TODO: M.100 read default environment from model, and unserialize it
        # TODO: M.100 read special environment
        # TODO: M.100 identify data to be filled out, and check completeness 
        # TODO: M.100 if error while model runtime data calculation, return without creating a thread
        # TODO: M.100 merge the defaultenvironment and the individual thread environment, special data wins
        # TODO: M.100 insert/create thread, TODO: RUNTIME_ENVIRONMENT : the environment....
        
        # create the thread
        thread_uuid = self.__decisionThreads.create_decision_thread_internal(dmuuid, model[DM_STARTNODE], ticketreference)
        thread_environment_uuid = self.__decisionThreadEnvironments.create_thread_environment({}, thread_uuid)
        self.__decisionThreads.set_fk_environment_uuid_for_thread_uuid(thread_uuid, thread_environment_uuid)
        
        return thread_uuid

    # ended according to the plan (e.g. end-node reached)
    def stop_decision_thread(self, thread_uuid):
        thread_data = self.__decisionThreads.select_decision_thread_by_uuid(thread_uuid)

        if thread_data is None:
            return None
        
        thread_data[DT_CURRENTSTATE] = RT_STATE_STOPPED

        # this whole thing shall be refactored when the main decision execution engine works
        self.__decisionThreads.update_decision_thread_by_uuid_iternal(thread_uuid, thread_data)


    # ended not to the plan (e.g. was terminated by someone
    def terminate_decision_thread(self, thread_uuid):
        # TODO: M.150: this stuff can be deleted manually for a while / also option to continue thread with another decision model
        # save thread to disk / archive??
        # delete from current database after archiving it
        pass

    
    ## TODO: get list of archived Threads?
    ## TODO: read information of archived Thread?
    
    # Process the special cases, the HIT provides extra human calculated data to the thread
    # HIT Human Itelligent Task
    # after a hit is invoked, the thread should be granted compute by calling 
    # process_single_decision_thread on that thread after a HIT node result and content was computed
    def process_HIT(self, thread_uuid, result):
        thread_data = self.__decisionThreads.select_decision_thread_by_uuid(thread_uuid)

        if thread_data is None:
            return None
        
        current_model_uuid = thread_data[DT_CURRENTMODEL]
        current_model_node = thread_data[DT_CURRENTNODE]
        
        model = self.__decisionModels.select_decision_model_by_uuid( current_model_uuid )
        node = model[DM_NODES][current_model_node]
        
        if not (node[DN_TYPE] == DN_TYPE_HIT):
            return None
        
        ## TODO: get thread environment by uuid
        ## check if environment is good / otherwise the thread must not be advanced
        
        if thread_data[DT_CURRENTSTATE] == RT_STATE_BLOCKED:
            
            ## TODO: calculate the method signature, so that the resultdata can be put in.
            ## TODO: process result data
            
            thread_data[DT_CURRENTSTATE] = RT_STATE_WAIT_FOR_TRANSIT
            # this whole thing shall be refactored when the main decision execution engine works
            self.__decisionThreads.update_decision_thread_by_uuid_iternal(thread_uuid, thread_data)
        
            
                
            ## TODO: transfer return data into the thread environment according to the signature data
            
            ## TODO: update thread environment
            
            pass
        
        pass
    
    # Process the specuak cases, the SYNC needs extra data for thre thread
    # SYNC - Synchronization Node, e.g. multiple HIT decisions requried, before it can continue
    # NOT YET 
    def process_SYNC(self, thread_uuid):
        pass

    
    # will compute one thread forward 
    def process_single_decision_thread(self, thread_uuid):
        # if no thread_uuid given 
        if not thread_uuid:
            return
        
        thread_data = self.__decisionThreads.select_decision_thread_by_uuid(thread_uuid)

        # if there is no thread data, we can stop here
        if thread_data is None:
            return

        # if the current state is blocked, that means it can not be processed further,
        # so we can stop here
        if thread_data[DT_CURRENTSTATE] == RT_STATE_BLOCKED:
            return
        
        
        running = True
        while running is True:
            # run the current node
            self.process_single_decision_node(thread_uuid)
            
            # reload the thread_data (information)
            thread_data = self.__decisionThreads.select_decision_thread_by_uuid(thread_uuid)
            
            if thread_data is None:
                running = False
                break;
            
            # check if the current state is Blocked or Waiting for Transit (after being advanced forward)
            # Waiting for transit means, that there might be an external event, which will make one of 
            # the transitions true, but none of them evaluate to true YET
            if (thread_data[DT_CURRENTSTATE] == RT_STATE_BLOCKED) or \
               (thread_data[DT_CURRENTSTATE] == RT_STATE_STOPPED) or \
               (thread_data[DT_CURRENTSTATE] == RT_STATE_WAIT_FOR_TRANSIT) :
                running = False
                break;
            pass
        pass

    # will compute one state forward 
    def process_single_decision_node(self, thread_uuid):
        if not thread_uuid:
            return
        
        thread_data = self.__decisionThreads.select_decision_thread_by_uuid(thread_uuid)

        # if there is no thread data, we can stop here
        if thread_data is None:
            return
        
        # we can stop, because it needs a human or sync interaction
        if thread_data[DT_CURRENTSTATE] == RT_STATE_BLOCKED:
            return
        
     
        ### -----------------
        ### Thread is stopped
        ### -----------------
        if thread_data[DT_CURRENTSTATE] == RT_STATE_STOPPED:
            # calculate number of direct childs. indirect - will be collected, through all stopped childthreads
            num_child_processes = self.__decisionThreads.select_count_child_decision_thread_by_uuid(thread_uuid)
            
            if num_child_processes > 0:
                child_threads = self.__decisionThreads.select_child_decision_threads_by_uuid(thread_uuid)
                
                # stop each one of them.
                for child_thread in child_threads:
                    if not (child_thread[DT_CURRENTSTATE ] == RT_STATE_STOPPED):
                        self.stop_decision_thread(child_thread[DT_UUID])
                return
            else:
                # kill it purge it, archive it, but only after all child threads are away 
                self.terminate_decision_thread(thread_uuid)
                return

        
        model = self.__decisionModels.select_decision_model_by_uuid(thread_data[DT_CURRENTMODEL])
        print(thread_data)
        ### -----------------
        ### Thread is started
        ### -----------------
        if  thread_data[DT_CURRENTSTATE] == RT_STATE_STARTED:
            start_node = self.__decisionModels.select_decision_node_from_decision_model(model, thread_data[DT_CURRENTNODE])
            
            # setup runtime state / prepare node processing, if thread was just started.
            if start_node[DN_TYPE] == DN_TYPE_HIT :
                thread_data[DT_CURRENTSTATE] = RT_STATE_BLOCKED
                
            elif start_node[DN_TYPE] == DN_TYPE_SYNC :
                thread_data[DT_CURRENTSTATE] = RT_STATE_BLOCKED
                
            elif start_node[DN_TYPE] == DN_TYPE_MIT :
                thread_data[DT_CURRENTSTATE] = RT_STATE_WAIT_FOR_COMPUTE
                
            # maybe I should remove the start state alltogether / since it provides not much value
            elif start_node[DN_TYPE] == DN_TYPE_START :
                thread_data[DT_CURRENTSTATE] = RT_STATE_WAIT_FOR_COMPUTE
                
            elif start_node[DN_TYPE] == DN_TYPE_END :
                thread_data[DT_CURRENTSTATE] = RT_STATE_STOPPED
                
            self.__decisionThreads.update_decision_thread_by_uuid_iternal(thread_uuid, thread_data)
        
        environment_uuid = thread_data[DT_ENVIRONMENT][DT_ENVIRONMENT_UUID]
        thread_environment = self.__decisionThreadEnvironments.select_thread_environment_by_uuid(environment_uuid)
        
        ### ----------------------------------
        ### Thread is waiting for compute time
        ### ----------------------------------
        if thread_data[DT_CURRENTSTATE] == RT_STATE_WAIT_FOR_COMPUTE:
            curent_node = self.__decisionModels.select_decision_node_from_decision_model(model, thread_data[DT_CURRENTNODE])

            # so lets execute the methods and its signature and then update the
            # thread and the thread_environment, since we computed some data for tthe thread to advance forward

            #TODO: self.evaluate_decision_node_method()
            # * Method
            # * Methodparameters
            # * thread runtime environment
            # * thread_data
            
            #TODO: thread_data should get a column 'lastcompute' having a timestamp
            #  fill lastcompute
            
            #TODO: update contents of the threadenvironment
            #TODO: maybe we have to rethink that... we should not override the environment this way.
            self.__decisionThreadEnvironments.update_decision_environment_by_uuid(environment_uuid, thread_environment )
            
            # advance runtime state
            thread_data[DT_CURRENTSTATE] = RT_STATE_WAIT_FOR_TRANSIT
            self.__decisionThreads.update_decision_thread_by_uuid_iternal(thread_uuid, thread_data) 
        
        
        # ok this node is waiting for a transition 
        if thread_data[DT_CURRENTSTATE] == RT_STATE_WAIT_FOR_TRANSIT:
            # get curent node from model
            current_node = self.__decisionModels.select_decision_node_from_decision_model(model, thread_data[DT_CURRENTNODE])
            
            transitions = current_node[DN_NEXTACTIONS]
            
            # ok we have to check each follownode and compute
            # whether we can do the transition
            for transition in transitions:
                #TODO: 
                # self.evaluate_decision_node_transition_method()
                # * Method
                # * Methodparameters
                # * thread runtime environment
                # * thread_data
                result = self.evaluate_decision_node_transition_method(transition, thread_data, thread_environment)
                
                if result is False:
                    continue
                
                if result is True:
                    follow_node_data = self.__decisionModels.select_decision_node_from_decision_model(model, transition[DNT_NEXT])
                    
                    if follow_node_data[DN_TYPE] == DN_TYPE_HIT:
                        thread_data[DT_CURRENTNODE] = follow_node_data[DN_UUID]
                        thread_data[DT_CURRENTSTATE] = RT_STATE_BLOCKED
                    elif follow_node_data[DN_TYPE] == DN_TYPE_SYNC:
                        thread_data[DT_CURRENTNODE] = follow_node_data[DN_UUID]
                        thread_data[DT_CURRENTSTATE] = RT_STATE_BLOCKED
                    elif follow_node_data[DN_TYPE] == DN_TYPE_MIT:
                        thread_data[DT_CURRENTNODE] = follow_node_data[DN_UUID]
                        thread_data[DT_CURRENTSTATE] = RT_STATE_WAIT_FOR_COMPUTE
                    elif follow_node_data[DN_TYPE] == DN_TYPE_END:
                        thread_data[DT_CURRENTNODE] = follow_node_data[DN_UUID]
                        thread_data[DT_CURRENTSTATE] = RT_STATE_STOPPED
                    
                    # TODO: copy the current environment data, which is required for the decision node
                    # TODO: copy the current environment data, which is required for the decision transition 
                    self.__decisionThreadEnvironments.append_transition_log_entry(
                        environment_uuid, 
                        self.strip_uuid(model[DM_UUID]), 
                        current_node[DN_UUID], 
                        transition[DNT_NAME], 
                        {})

                    # TODO: Transitions should not write back to the environment other than 
                    #       logging for the reports - but it is undecided where this goes...
                    # TODO: maybe we have to rethink this, we should not work this way on the environment
                    self.__decisionThreadEnvironments.update_decision_environment_by_uuid(
                        environment_uuid, 
                        thread_environment )

                    
                    # contains the new current state and the new current node 
                    self.__decisionThreads.update_decision_thread_by_uuid_iternal(
                        thread_uuid, 
                        thread_data)
                    
                    # break the transition search, after we found a successful node.
                    break
            
            # endfor transitions
            pass
        # endif wait for transit
        pass
    
    def strip_uuid(self, uuid):
        if(uuid.startswith("DM_") or uuid.startswith("DN_")) :
            return uuid[3:]
        else:
            if(uuid.startswith("KBA_")):
                return uuid[4:]
        return uuid

     
    # evaluated one decision node calculation 
    def evaluate_decision_node_method(self):
        # TODO: calculate the signature of the method to invoke
        
        # TODO: use the trhead eviromnent to prepare the proper method call
        # TODO: import stuff and such...
        # TODO: check method existence
        # TODO: invoke methods / a.k.a. eval
        
        # TODO: check the result value for existence otherwise return neutral value 
        pass

    # evaluates one transition, and tells whether this applies... / First True wins
    def evaluate_decision_node_transition_method(self, transition, thread_data, thread_environment):
        if not DNT_GUARD_SIGNATURE in transition:
            return  False

        method_signature = transition[DNT_GUARD_SIGNATURE]

        # idea is to use something like this... we load a predefined package + module then find the function and call it
        value = False
        vm_transitions_module = importlib.import_module('.transitions', package='de.mindscan.cheaplithium.vm')
        print("module: {}".format(vm_transitions_module))
        func = getattr(vm_transitions_module,'isFalse')
        print("func: {}".format(func))
        result = func(value)
        print("result: {}".format(result))

        # TODO: calculate the methods to invoke and their parameters 
        
        # TODO: use the trhead eviromnent to prepare the proper method call
        # TODO: import stuff and such...
        # TODO: check method existence
        # TODO: invoke methods / a.k.a. eval
        # TODO: also check if the template contains required data.
        
        # update environment according to collected signature references
        # return the apiresult and the api data

        # ATTN: this will let the decision model always take the first transition 
        return True
    
    # TODO: do the signature splitting and such?
    # or get from a json array? instead of parsing signatures and stuff...
    # have transition signatures
    # have node sinatures
    
