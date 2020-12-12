'''
Created on 21.11.2020

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
SRC_BASE_DIR  = '../../../../../src'
DATA_BASE_DIR = '../../../../../data'

import sys
sys.path.insert(0,SRC_BASE_DIR)

import json
import uuid as uid

from fastapi import FastAPI, Form

app = FastAPI()


# import the data model column names / property names
from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport
from de.mindscan.cheaplithium.datamodel.DecisionModel import DecisionModel
from de.mindscan.cheaplithium.datamodel.DecisionThread import DecisionThread

DATAMODEL_DIR = DATA_BASE_DIR + '/cheaplithium/dm/'
DATATHREAD_DIR = DATA_BASE_DIR + '/cheaplithium/threads/'

# -----------------------------------------
# DecisionModel "Database"
# -----------------------------------------
 
decisionModels = DecisionModel(DATAMODEL_DIR)
decisionThreads = DecisionThread(DATATHREAD_DIR)

# -----------------------------------------
# Later extract the decision modelling code
# -----------------------------------------
def create_successful_uuid_result(uuid:str):
    return {"uuid":uuid, "isSuccess":True, "isError":False}

def strip_uuid(uuid):
    if(uuid.startswith("DM_") or uuid.startswith("DN_")) :
        return uuid[3:]
    return uuid

# --------------------------------------
# API-Webserver "code" - 
# --------------------------------------

@app.get("/")
def read_root():
    return {"message":"Hello World! It works! But now, go away!"}


@app.get("/CheapLithium/rest/getDecisionModel/{uuid}")
async def provide_decision_model( uuid:str='0518f24f-41a0-4f13-b5f6-94a015b5b04c'):
    try:
        read_uuid = uid.UUID('{' + uuid + '}')
    except:
        return {"messsage":"invalid uuid"}
    
    if ( str(read_uuid) == uuid):
        return decisionModels.provide_decision_model_internal(uuid)
    else:
        return  {"message":"uuid doesn't match."}
    
    return {}


@app.post("/CheapLithium/rest/createDecisionModel")
async def create_decision_model( name:str = Form(...), displayname:str=Form(...), 
    description:str=Form(...), version:str = Form(...)):
    
    _, uuid  = decisionModels.create_decision_model_internal(name, displayname, description, version)
    
    return create_successful_uuid_result(uuid)


@app.post("/CheapLithium/rest/createDecisionNode")
async def create_decision_node (name:str = Form(...), exectype:str = Form(...), 
                                kbarticle:str = Form(""), dmuuid:str=Form(...)):
    dmuuid = strip_uuid(dmuuid)
    
    dnode, _ = decisionModels.create_decision_node_internal(name, exectype, kbarticle, [])
    decisionModels.insert_decision_node_into_decision_model(dnode, dmuuid)
    
    return create_successful_uuid_result(dmuuid)


@app.post("/CheapLithium/rest/persistDecisionModel")
async def persist_decision_model ( uuid: str = Form(...)):
    dmuuid = strip_uuid(uuid)
    
    try:
        read_uuid = uid.UUID('{' + dmuuid + '}')
    except:
        return {"messsage":"invalid uuid"}
    
    if ( str(read_uuid) == dmuuid):
        if decisionModels.isInDatabase(dmuuid):
            decisionModels.persist_decision_model_internal(dmuuid)
        
    return create_successful_uuid_result(dmuuid)


@app.get("/CheapLithium/rest/getDecisionModelList")
async def get_decision_model_list():
    return decisionModels.select_decision_models_from_backend()
    

@app.post("/CheapLithium/rest/insertDecisionNodeTransition")
async def insert_decision_node_transition(uuid: str = Form(...), dnuuid:str=Form(...), transition:str=Form(...)):
    transitionObject = json.loads(transition)
    
    uuid = strip_uuid(uuid)
    
    if decisionModels.isInDatabase(uuid):
        decisionModels.insert_decision_node_transition_internal(uuid, dnuuid,  transitionObject)
    else:
        print({"message", "uuid_not in database"})
        return {"message", "uuid_not in database"}
    
    return create_successful_uuid_result(uuid)


@app.post("/CheapLithium/rest/updateDecisionNodeTransition")
async def update_decision_node_transition(uuid: str = Form(...), dnuuid:str=Form(...), index:int=Form(...), transition:str=Form(...)):
    transitionObject = json.loads(transition)

    uuid = strip_uuid(uuid)
    
    if decisionModels.isInDatabase(uuid):
        decisionModels.update_decision_node_transitrion_internal(uuid, dnuuid, index, transitionObject)
    else:
        print({"message", "uuid_not in database"})
        return {"message", "uuid_not in database"}
    
    return create_successful_uuid_result(uuid)
          

@app.post("/CheapLithium/rest/updateDecisionNode")
async def update_decision_node( uuid:str=Form(...), dnuuid:str=Form(...), name:str=Form(...), exectype:str=Form(...), kbarticle:str=Form("")):
    uuid = strip_uuid(uuid)
    
    if decisionModels.isInDatabase(uuid):
        decisionModels.update_decision_node_internal(uuid, dnuuid, name, exectype, kbarticle)
    else:
        print({"message", "uuid_not in database"})
        return {"message", "uuid_not in database"}
    
    return create_successful_uuid_result(uuid)


@app.post("/CheapLithium/rest/updateDecisionModel")
async def update_decision_model(uuid: str = Form(...), name:str = Form(...),  displayname:str=Form(...), 
    description:str=Form(...), version:str = Form(...)):
    
    uuid = strip_uuid(uuid)
    
    if decisionModels.isInDatabase(uuid):
        decisionModels.update_decision_model_internal(uuid, name, displayname, description, version)
    else:
        print({"message", "uuid_not in database"})
        return {"message", "uuid_not in database"}
    
    return create_successful_uuid_result(uuid)

##
## Unfinished yet
##


@app.post("/CheapLithium/rest/cloneDecisionModel")
async def clone_decision_model(uuid: str = Form(...)):
    # clone/copy that model, but create different uuids for each element
    # clone that model in the dictionary... - no persistence required 
    
    return create_successful_uuid_result(uuid)


##
##
## Thread-"database"
##
##

@app.get("/CheapLithium/rest/getDecisionThread/{uuid}")
async def provide_decision_thread(uuid: str='b5ef3ee2-e059-458f-b8a4-77ce7301fef0'):
    try:
        read_uuid = uid.UUID('{' + uuid + '}')
    except:
        return {"message":"invalid uuid"}
        
    if( str(read_uuid) == uuid):
        return DecisionThread.provide_decision_thread_internal(uuid)
    else:
        return {"message":"uuid doesn't match."}
     
    return {}


@app.get("/CheapLithium/rest/getDecisionThreadList")
async def get_decision_thread_list():
    return decisionThreads.select_all_from_decision_threads();


@app.post("/CheapLithium/rest/startDecisionThread")
async def create_decision_thread(uuid:str=Form(...), ticketreference:str = Form("")):
    dmuuid = strip_uuid(uuid)
    
    dm = decisionModels.provide_decision_model_internal(dmuuid)
    startnode = dm[DM_STARTNODE];
    
    threadUuid = decisionThreads.create_decision_thread_internal(dmuuid, startnode, ticketreference)
    
    # TODO: use execution engine for initial run until halt...
    
    return create_successful_uuid_result(threadUuid)
    