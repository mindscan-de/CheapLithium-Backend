'''
Created on 12.12.2020

@author: JohnDoe
'''
import os
import json
import uuid as uid

from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport

baseThreads = [
                {
                    DT_UUID : "b5ef3ee2-e059-458f-b8a4-77ce7301fef0",
                    DT_ENVIRONMENT : {
                            "uuid":"2a33075e-4677-4f98-b1fb-c87dd6437263",
                            "log":[],
                            "nodehistory" : []
                        },
                    DT_CURRENTSTATE : "STATE/WAIT/RUNNING/TERMINATED",
                    DT_CURRENTMODEL : "0518f24f-41a0-4f13-b5f6-94a015b5b04c",
                    DT_CURRENTNODE : "DN_559e9bf8-242e-4887-86fa-f3427647f1cb",
                    DT_TICKETFERENCE : [
                        "NSSXMI-26940","NSSXMI-17262"
                        ],
                    DT_OWNER: ""
                }
            ]


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
        
    def provide_decision_thread_internal(self,uuid:str):
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
                return {"message":"no_such_persisted_thread"}

    def create_decision_thread_internal(self, dmuuid, startnode, ticketreference):
        threadUuid = str(uid.uuid4())
        
        newThread = {
            DT_UUID:str(threadUuid), 
            DT_ENVIRONMENT:{}, 
            DT_CURRENTSTATE:"START", 
            DT_CURRENTMODEL:dmuuid, 
            DT_CURRENTNODE:startnode, 
            DT_TICKETFERENCE:[ticketreference], 
            DT_OWNER:""}
        
        self.__inMemoryDatabase[threadUuid] = newThread
        
        return threadUuid
    
    # TODO: implement the decisionlist by crawling the keys of the Database and join it with the filenames of the directory.

    def select_all_from_decision_threads(self):
        global baseThreads
        threads = baseThreads.copy()
        
        for _,value in self.__inMemoryDatabase.items():
            threads.append( value );
            
        return {
            "threads" : threads 
            }
    
