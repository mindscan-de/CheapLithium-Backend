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
import os
import json
import time
import uuid as uid

from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport

class DecisionThread(object):
    '''
    classdocs
    '''


    def __init__(self, datathread_dir = ''):
        '''
        Constructor
        '''
        self.__datathread_directory = datathread_dir
        self.__inMemoryDatabase = {}
        
    def select_decision_thread_by_uuid(self,uuid:str):
        if uuid in self.__inMemoryDatabase:
            return self.__inMemoryDatabase[uuid]
        else:
            jsonfilepath = self.__datathread_directory + uuid + '.json'
            if os.path.isfile(jsonfilepath):
                with open(jsonfilepath) as json_source_file:
                    tmpDecisionThread = json.load(json_source_file)
                    self.__inMemoryDatabase[uuid] = tmpDecisionThread
                    return tmpDecisionThread
            else:
                return None

    def load_all_threads(self):
        for file in os.listdir(self.__datathread_directory):
            if str(file).endswith(".json"):
                uuid, _ = os.path.splitext(file)
                self.select_decision_thread_by_uuid(uuid)
    

    def create_decision_thread_internal(self, dmuuid, startnode, ticketreference):
        threadUuid = str(uid.uuid4())
        
        # TODO: create an empty decision Thread environment... and use its UUID here...
        newThread = {
            DT_UUID:str(threadUuid), 
            DT_ENVIRONMENT:{
                DT_ENVIRONMENT_UUID:""
                }, 
            DT_CURRENTSTATE:RT_STATE_STARTED, 
            DT_CURRENTMODEL:dmuuid, 
            DT_CURRENTNODE:startnode, 
            DT_TICKETFERENCE:[ticketreference], 
            DT_OWNER:"",
            DT_CREATED: str(time.time()),
            DT_MODIFIED: "",
            DT_FINALIZED: ""
            }
        
        self.__inMemoryDatabase[threadUuid] = newThread
        self.save_to_disk(threadUuid)
        
        return threadUuid
    
    ## ATTENTION this is not for public use, i will refactor it 
    ## when the decision engine workd
    ## TODO: add update modified date...
    def update_decision_thread_by_uuid_iternal(self, thread_uuid:str, thread_data):
        self.__inMemoryDatabase[thread_uuid] = thread_data
        self.save_to_disk(thread_uuid)
        #TODO: SAVE to disk...
        
    def save_to_disk(self, thread_uuid):
        jsonfilepath = self.__datathread_directory + thread_uuid + '.json'
        
        with open(jsonfilepath,"w") as json_target_file:
            json.dump(self.__inMemoryDatabase[thread_uuid], json_target_file,indent=2);

    
    # TODO: implement the decisionlist by crawling the keys of the Database and join it with the filenames of the directory.
    
    # TODO: M.200 - calculate the number of child threads (direct) and subthreads 
    #               (indirect - will be collected, through all stopped childthreads)
    def select_count_child_decision_thread_by_uuid(self, thread_uuid):
        return 0
    
    # TODO: M.200 - collect the direct sub threads 
    def select_child_decision_threads_by_uuid(self, thread_uuid):
        return []

    def select_all_from_decision_threads(self):
        threads = []
        for key,value in self.__inMemoryDatabase.items():
            threads.append( {
                    DT_UUID: key,
                    DT_CURRENTSTATE: value[DT_CURRENTSTATE],
                    DT_CURRENTMODEL: value[DT_CURRENTMODEL],
                    DT_CURRENTNODE: value[DT_CURRENTNODE],
                    DT_TICKETFERENCE: value[DT_TICKETFERENCE],
                    DT_CREATED: value[DT_CREATED],
                    DT_MODIFIED: value[DT_MODIFIED],
                    DT_FINALIZED: value[DT_FINALIZED]
                } );
            
        return {
            "threads" : threads 
            }
    
    def set_fk_environment_uuid_for_thread_uuid(self, thread_uuid, environment_uuid):
        thread = self.select_decision_thread_by_uuid(thread_uuid)
        thread[DT_ENVIRONMENT][DT_ENVIRONMENT_UUID] = environment_uuid
        self.update_decision_thread_by_uuid_iternal(thread_uuid, thread)
        