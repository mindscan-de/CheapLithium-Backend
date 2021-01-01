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
import re
import importlib
import sys

# import the data model column names / property names
from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport
# import the data tables / access to data on a amore abstract level
from de.mindscan.cheaplithium.datamodel.DecisionModel import DecisionModel
from de.mindscan.cheaplithium.datamodel.DecisionThread import DecisionThread
from de.mindscan.cheaplithium.datamodel.DecisionThreadEnvironments import DecisionThreadEnvironments


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
            current_node = self.__decisionModels.select_decision_node_from_decision_model(model, thread_data[DT_CURRENTNODE])

            # so lets execute the method(s) and its signature and then update the
            # thread and the thread_environment, since we computed some data for the thread to advance forward
            try:
                result, result_data = self.evaluate_decision_node_method(current_node, thread_data, thread_environment)
            except:
                # TODO: maybe we should do something else, but for now it is better to have it like this.
                return
            
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
            # whether we can follow the transition
            for transition in transitions:
                result = False
                try:
                    result, result_data = self.evaluate_decision_node_transition_method(transition, thread_data, thread_environment)
                except:
                    e,_,traceback = sys.exc_info()
                    # ATTN: will update the thread_environment - 
                    thread_environment = \
                        self.__decisionThreadEnvironments.append_error_log_entry(
                            environment_uuid, 
                            'error', 
                            'Exception triggererd while evaluating the decision_node transition for transition: named: {}'.format(transition[DNT_NAME]), 
                            { 
                                'exception':str(e),
                                'traceback':str(traceback)
                            })
                    continue
                
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
                    
                    self.__decisionThreadEnvironments.append_transition_log_entry(
                        environment_uuid, 
                        self.strip_uuid(model[DM_UUID]), 
                        current_node[DN_UUID], 
                        transition[DNT_NAME], 
                        result_data)

                    # contains the new current state and the new current node 
                    self.__decisionThreads.update_decision_thread_by_uuid_iternal(
                        thread_uuid, 
                        thread_data)
                    
                    # break transition search, after we found a successful node.
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
    def evaluate_decision_node_method(self, decision_node, thread_data, thread_environment):
        if not DN_MIT_SIGNATURE in decision_node:
            # TODO: we should log that this is an incoplete model
            # TODO: we should raise an exception instead of returning
            # TODO: maybe add that to the thread errors list
            return None, None
        
        # calculate the signature of the method to invoke
        method_name, method_parameters_info = self.parse_node_mit_signature(decision_node[DN_MIT_SIGNATURE])
        
        if method_name is None:
            # problem is for a MIT Node, there should be a real signature, even when it is nop() or so.
            return None, None
        
        method_parameters = self.convert_method_parameter_info(method_parameters_info, thread_environment)
        
        result, result_data = self.invoke_mit_method(self, method_name, method_parameters)
        
        # TODO: evaluate the "method body" of the MIT-signature
        # TODO: We might now return also an update packet wor the environment? 
        return result, result_data

    
    # TODO: parse node MIT signature 
    def parse_node_mit_signature(self, node_mit_signature:str):
        return None, None
    
    
    def invoke_mit_method(self, method_name, method_parameters, ):
        # TODO: import stuff and such...
        # TODO: check method body existence
        # TODO: invoke methods / a.k.a. eval
        return None, None
        
    
    # TODO: parse node HIT signature    
    def parse_node_hit_signature(self, node_hit_signature:str):
        return
    
    
    # ################################
    # Transition Handling
    # ################################
    
    
    def evaluate_decision_node_transition_method(self, transition, thread_data, thread_environment):
        if not DNT_GUARD_SIGNATURE in transition:
            return  False

        # calculate the method to invoke and their parameters 
        method_name, method_parameters_info, method_body = self.parse_guard_signature(transition[DNT_GUARD_SIGNATURE])
        
        if method_name is None:
            return False
        
        # convert the parameters to their correct type and such
        method_parameters = self.convert_method_parameter_info(method_parameters_info, thread_environment)
        
        # invoke the calculated method
        result = self.invoke_transition_method(method_name, method_parameters)

        transition_data = {}
        if result is True:
            transition_data = self.evaluate_decision_node_transition_method_body(method_body, thread_data, thread_environment)
        
        return result, transition_data
    

    # transition.isTrue(env.XXY) { data: IN:OUT SIGNATURE_DATA, ...}
    # transition.isEqual(env.XYY, 50) { data: IN:OUT SIGNATURE, }
    # transition.isGreaterOrEqual(a,b ) { }
    # transition.isLessOrEqual(a,b) {}
    # transition.isGreater(a,b) {}
    # transition.isLess(a,b) {}
    def parse_guard_signature(self, guard_signature:str):
        # Much more useful would be an EXPRESSION AST, but currently we don't need that mode of processing signatures
        # Because i would invoke a lexer which creates tokens and then parse the tokens to build the AST and return it
                
        # Signature spliting: we only need something simple right now. 
        result = re.match("(.*)\((.*?)\)(.*)", guard_signature)
        if result is None:
            return None, None, None
        
        transition_method = result.group(1)
        transition_method_parameters = result.group(2)
        transition_method_body = result.group(3) 
        
        print("\ntransition method: {}".format(transition_method))
        print("\ntransition parameters: {}".format(transition_method_parameters))
        print("\ntransition method body: {}".format(transition_method_body))
        
        # for methods with no parameters
        if not transition_method_parameters :
            return transition_method, [], transition_method_body
        
        splitted_transition_method_parameters = transition_method_parameters.split(",")
        
        return transition_method, splitted_transition_method_parameters, transition_method_body
    
    
    def convert_method_parameter_info(self, method_parameters_info, thread_environment):
        if method_parameters_info is None:
            return []
        
        result = []
        for parameter_info in method_parameters_info:
            result.append(self.convert_single_method_parameter(parameter_info, thread_environment))
        
        return result
    
    
    def convert_single_method_parameter(self, parameter_info:str, thread_environment:dict):
        parameter_info = parameter_info.strip();
        
        # match true
        if   parameter_info.lower() == "true" : 
            return True 
        # match false
        elif parameter_info.lower() == "false":
            return False
        # match none type
        elif parameter_info.lower() == "none":
            return None
        # match numbers
        elif re.match("[-+]?\d+", parameter_info):
            return int(parameter_info)
        # use the thread environment as source of truth...
        elif parameter_info.startswith("env."):
            # we can currently not subindex, but this should be possible in future (ato de) 
            key = parameter_info[len("env."):]
            return thread_environment[DTE_RTE_DATA][key]
        # thread data, is there something interesting ? 
        elif parameter_info.startswith("thread."):
            # maybe later implement access to thread data (ato de)
            pass
        
        # just keep that as a string for now.
        return parameter_info

    
    
    def invoke_transition_method(self, method_name, method_parameters):
        # load a predefined package + module 
        vm_transitions_module = importlib.import_module('.transitions', package='de.mindscan.cheaplithium.vm')
        
        # find the function - it will raise an exception if method_name doesn't exist
        func = getattr(vm_transitions_module, method_name)
        # print("\nfunc: {}".format(func))
        
        # invoke method
        result = func(*method_parameters)
        return result


    def evaluate_decision_node_transition_method_body(self, method_body, thread_data, thread_environment):
        if not method_body:
            return {}
        
        # TODO: evaluate "method_body" and calculate transition_data
        # also check if the method body template contains required data - should be calculated if result is true
        
        # TODO: also parse the method "body", consider this as a data conversion layer, 
        #       which is important for the data field of the transition, so data fields from the node calculation can
        #       be taken over to the template content for the thread report.
        
        parsed_method_body = self.parse_decision_nodetransition_method_body(method_body)
        
        # TODO: convert parsed method_body into
        data = {} 

        return data
    
    
    def parse_decision_nodetransition_method_body(self, method_body):
        # TODO: result should be a dictionary with keys being strings and values being strings, which will be
        # evaluated by a replacement method. 
        return {}
    
    
