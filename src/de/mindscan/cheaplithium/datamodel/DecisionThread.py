'''
Created on 12.12.2020

@author: JohnDoe
'''
import os
import json
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
