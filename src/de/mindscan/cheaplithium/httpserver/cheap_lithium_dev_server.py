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
import os.path

from fastapi import FastAPI, Form

app = FastAPI()



# import the data model column names / property names
from de.mindscan.cheaplithium.datamodel.consts import *

DATAMODEL_DIR = DATA_BASE_DIR + '/cheaplithium/dm/'
DATATHREAD_DIR = DATA_BASE_DIR + '/cheaplithium/threads/'


# -----------------------------------------
# DecisionModel "Database"
# -----------------------------------------
# persist only as long as the server is 
# runing, for development, we don't need 
# database support yet. Maybe never?
# -----------------------------------------
 
decisionModelDatabase = {}
decisionThreadDatabase = {}

# -----------------------------------------
# Later extract the decision modelling code
# -----------------------------------------
def create_successful_uuid_result(uuid:str):
    return {"uuid":uuid, "isSuccess":True, "isError":False}

def strip_uuid(uuid):
    if(uuid.startswith("DM_") or uuid.startswith("DN_")) :
        return uuid[3:]
    return uuid


def create_decision_node_transition_internal( name, nextnodeuuid, template):
    return { 
        DNT_NAME: name, 
        DNT_NEXT: nextnodeuuid, 
        DNT_TEMPLATE: template }

def create_decision_node_internal(dnname, dntype, kbarticle, dnfollownodes):
    dnUuid = uid.uuid4()
    decisionNode = {
        DN_UUID: 'DN_' + str(dnUuid), 
        DN_NAME: dnname , 
        DN_TYPE: dntype , 
        DN_KBARTICLE: kbarticle ,
        DN_NEXTACTIONS: []}
    
    if len(dnfollownodes) >= 1:
        if(len(dnfollownodes)) == 1:
            tn = create_decision_node_transition_internal('default', dnfollownodes[0][DN_UUID], '')
            decisionNode[DN_NEXTACTIONS].append(tn)
        else:
            pass
    
    return decisionNode, str(dnUuid)

def create_decision_model_internal(name:str, displayname:str, description:str, version:str):
    dmUuid = uid.uuid4()
    
    endnode, _ = create_decision_node_internal('900.endstate',DN_TYPE_END,'',[])  
    startnode, _ = create_decision_node_internal('000.startstate',DN_TYPE_START,'',[endnode])

    decisionModel = {
        DM_UUID: 'DM_' + str(dmUuid), 
        DM_NAME: name, 
        DM_DISPLAYNAME: displayname, 
        DM_VERSION: version, 
        DM_DESCRIPTION: description, 
        DM_STARTNODE: startnode[DN_UUID],
        DM_NODES: [startnode, endnode]}
    
    return  decisionModel, str(dmUuid)

def insert_decision_node_into_decision_model(dn, dmuuid:str):
    global decisionModelDatabase
    
    decisionModel = decisionModelDatabase[dmuuid]
    nodes = decisionModel[DM_NODES]
    nodes.append(dn)
    #  sort decision nodes by name (good enough) 
    sortednodes = sorted(nodes, key=lambda k: k['name'])
    decisionModel[DM_NODES] = sortednodes
     
    decisionModelDatabase[dmuuid] = decisionModel
    
    return decisionModel, dmuuid


def persist_decision_model_internal(dmuuid):
    global decisionModelDatabase
    try:
        read_uuid = uid.UUID('{' + dmuuid + '}')
    except:
        return {"messsage":"invalid uuid"}

    if ( str(read_uuid) == dmuuid):
        jsonfilepath = DATAMODEL_DIR + str(read_uuid) + '.json'
        
        if dmuuid in decisionModelDatabase:
            with open(jsonfilepath,"w") as json_target_file:
                json.dump(decisionModelDatabase[dmuuid], json_target_file,indent=2);
        
        pass
        
    return dmuuid

# --------------------------------------
# API-Webserver "code" - 
# --------------------------------------

@app.get("/")
def read_root():
    return {"message":"Hello World! It works! But now, go away!"}

@app.get("/CheapLithium/rest/getDecisionModel/{uuid}")
async def provide_decision_model( uuid:str='0518f24f-41a0-4f13-b5f6-94a015b5b04c'):
    global decisionModelDatabase
    try:
        read_uuid = uid.UUID('{' + uuid + '}')
    except:
        return {"messsage":"invalid uuid"}
    
    if ( str(read_uuid) == uuid):
        if uuid in decisionModelDatabase:
            return decisionModelDatabase[uuid]
        else:
            jsonfilepath = DATAMODEL_DIR + str(read_uuid) + '.json'
            if os.path.isfile(jsonfilepath):
                with open(jsonfilepath) as json_source_file:
                    tmpDecisionModel = json.load(json_source_file)
                    decisionModelDatabase[uuid] = tmpDecisionModel
                    return tmpDecisionModel
            else:
                return {"message":"no_such_persisted_model "}
    else:
        return  {"message":"uuid doesn't match."}
    
    return {}

@app.post("/CheapLithium/rest/createDecisionModel")
async def create_decision_model( name:str = Form(...), displayname:str=Form(...), 
    description:str=Form(...), version:str = Form(...)):
    global decisionModelDatabase
    
    # Create and Cache the model until restart
    model, uuid  = create_decision_model_internal(name, displayname, description, version)
    decisionModelDatabase[uuid] =  model
    
    return create_successful_uuid_result(uuid)

@app.post("/CheapLithium/rest/createDecisionNode")
async def create_decision_node (name:str = Form(...), exectype:str = Form(...), 
                                kbarticle:str = Form(""), dmuuid:str=Form(...)):
    global decisionModelDatabase
    
    dmuuid = strip_uuid(dmuuid)
    
    dnode, _ = create_decision_node_internal(name, exectype, kbarticle, [])
    insert_decision_node_into_decision_model(dnode, dmuuid)
    
    # return back to model
    return create_successful_uuid_result(dmuuid)

@app.post("/CheapLithium/rest/persistDecisionModel")
async def persist_decision_model ( uuid: str = Form(...)):
    global decisionModelDatabase
    
    uuid = strip_uuid(uuid)
    persist_decision_model_internal(uuid)
    
    return create_successful_uuid_result(uuid)


# TODO: implement the listing by crawling the keys of the Database and join it with the filenames of the directory.
#       also skip files, which keys are already present in the list -> no deseialization needed.
#       in future use a database and use SQL and/or NOSQL, but for this approach, we really don't need a database at this stage.

@app.get("/CheapLithium/rest/getDecisionModelList")
async def get_decision_model_list():
    # 2020-11-29:
    # this is just a crude hack, but there is no reason to implement an index of the models right now.
    # ... only want to bootstrap something else right now. no need to implement a solution at the moment 
    return  {
        "items": [
            {
                "uuid": "0518f24f-41a0-4f13-b5f6-94a015b5b04c",
                "name": "MyGlasswallDecisionModel",
                "displayname": "My Glasswall Decision Model",
                "version": "1.0",
                "description":"This model helps to analyze issues generated by me - Glasswall"
            },
            {
                "uuid": "bfb2e592-bd77-433e-8ea7-9e630939ae72", 
                "name": "MyModel", 
                "displayname": "My Model is best Model", 
                "version": "1.0", 
                "description": "This Model will make you smarter. Promised!"                
            },
            {
                 "uuid": "fa4c1a38-26f3-41c7-be76-bee7b2e0e9cb", 
                 "name": "MyModel", 
                 "displayname": "This is only my decond best mdel", 
                 "version": "2.0", 
                 "description": "But this will make you even more smarter."
            },
            {
                "uuid": "db60a6a3-97c6-4f51-8513-b4751c650eb4", 
                "name": "ChoosingTheRightEstimator", 
                "displayname": "Choosing the right Estimator", 
                "version": "1.0", 
                "description": "Often the hardest part of solvind a machine learning problem can be finding the right estimator for the job.\r\nDifferent estimators are better suited for different types of data and differen problems.\r\nThe decision tree is designed to give usera a bit of a rough guide on how to approach problems with regard to which estimators to try on your data."
            } 
            ]}

@app.post("/CheapLithium/rest/insertDecisionNodeTransition")
async def insert_decision_node_transition(uuid: str = Form(...), dnuuid:str=Form(...), transition:str=Form(...)):
    global decisionModelDatabase
    transitionObject = json.loads(transition)
    
    uuid = strip_uuid(uuid)
    
    if uuid in decisionModelDatabase:
        decisionModel = decisionModelDatabase[uuid]
        for decisionNode in decisionModel[DM_NODES]:
            if decisionNode[DN_UUID] == dnuuid:
                decisionNode[DN_NEXTACTIONS].append(transitionObject)
    else:
        print({"message", "uuid_not in database"})
        return {"message", "uuid_not in database"}
    
    
    
    return create_successful_uuid_result(uuid)

@app.post("/CheapLithium/rest/updateDecisionNodeTransition")
async def update_decision_node_transition(uuid: str = Form(...), dnuuid:str=Form(...), index:int=Form(...), transition:str=Form(...)):
    global decisionModelDatabase 
    transitionObject = json.loads(transition)

    uuid = strip_uuid(uuid)
    
    if uuid in decisionModelDatabase:
        decisionModel = decisionModelDatabase[uuid]
        for decisionNode in decisionModel[DM_NODES]:
            if decisionNode[DN_UUID] == dnuuid:
                decisionNode[DN_NEXTACTIONS][index]=transitionObject
                break;
    else:
        print({"message", "uuid_not in database"})
        return {"message", "uuid_not in database"}
    
    return create_successful_uuid_result(uuid)          

@app.post("/CheapLithium/rest/updateDecisionNode")
async def update_decision_node( uuid:str=Form(...), dnuuid:str=Form(...), name:str=Form(...), exectype:str=Form(...), kbarticle:str=Form("")):
    global decisionModelDatabase
    
    uuid = strip_uuid(uuid)
    
    if uuid in decisionModelDatabase:
        decisionModel = decisionModelDatabase[uuid]
        for decisionNode in decisionModel[DM_NODES]:
            if decisionNode[DN_UUID] == dnuuid:
                decisionNode[DN_NAME] = name
                decisionNode[DN_TYPE] = exectype
                decisionNode[DN_KBARTICLE] = kbarticle
                break;
    else:
        print({"message", "uuid_not in database"})
        return {"message", "uuid_not in database"}
    
    return create_successful_uuid_result(uuid)

@app.post("/CheapLithium/rest/updateDecisionModel")
async def update_decision_model(uuid: str = Form(...), name:str = Form(...),  displayname:str=Form(...), 
    description:str=Form(...), version:str = Form(...)):
    
    uuid = strip_uuid(uuid)
    
    if uuid in decisionModelDatabase:
        decisionModel = decisionModelDatabase[uuid]
        decisionModel[DM_NAME] = name
        decisionModel[DM_DISPLAYNAME] = displayname
        decisionModel[DM_DESCRIPTION] = description
        decisionModel[DM_VERSION] = version
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

# TODO: implement the cache layer seaparately, and split reading the data from disk - this code is ugly - but it still does what it should. (Was just hacked down) 

@app.get("/CheapLithium/rest/getDecisionThread/{uuid}")
async def provide_decision_thread(uuid: str='b5ef3ee2-e059-458f-b8a4-77ce7301fef0'):
    global decisionThreadDatabase
    try:
        read_uuid = uid.UUID('{' + uuid + '}')
    except:
        return {"message":"invalid uuid"}
        
    if( str(read_uuid) == uuid):
        if uuid in decisionThreadDatabase:
            return decisionThreadDatabase[uuid]
        else:
            jsonfilepath = DATATHREAD_DIR + str(read_uuid) + '.json'
            if os.path.isfile(jsonfilepath):
                with open(jsonfilepath) as json_source_file:
                    tmpDecisionThread = json.load(json_source_file)
                    decisionThreadDatabase[uuid] = tmpDecisionThread
                    return tmpDecisionThread
            else:
                return {"message":"no_such_persisted_thread"}
    else:
        return {"message":"uuid doesn't match."}
     
    return {}

# TODO: implement the decisionlist by crawling the keys of the Database and join it with the filenames of the directory.

baseThreads = [
                {
                    "uuid" : "b5ef3ee2-e059-458f-b8a4-77ce7301fef0",
                    "environment" : {
                            "uuid":"2a33075e-4677-4f98-b1fb-c87dd6437263",
                            "log":[],
                            "nodehistory" : []
                        },
                    "currentstate" : "STATE/WAIT/RUNNING/TERMINATED",
                    "currentmodel" : "0518f24f-41a0-4f13-b5f6-94a015b5b04c",
                    "currentnode" : "DN_559e9bf8-242e-4887-86fa-f3427647f1cb",
                    "ticketreference" : [
                        "NSSXMI-26940","NSSXMI-17262"
                        ],
                    "owner": ""
                }
            ]

@app.get("/CheapLithium/rest/getDecisionThreadList")
async def get_decision_thread_list():
    global baseThreads
    threads = baseThreads.copy()
    
    global decisionThreadDatabase 
    for _,value in decisionThreadDatabase.items():
        threads.append( value );
        
    return {
        "threads" : threads 
        }

@app.post("/CheapLithium/rest/startDecisionThread")
async def create_decision_thread(uuid:str=Form(...), ticketreference:str = Form("")):
    global decisionThreadDatabase;
    
    dmuuid = strip_uuid(uuid)
    
    # load decisionModel information by
    # calculate startnode
    startnode = "XXY";
    
    threadUuid = str(uid.uuid4())
    
    newThread={
            DT_UUID : str(threadUuid),
            DT_ENVIRONMENT : {},
            DT_CURRENTSTATE : "START",
            DT_CURRENTMODEL : dmuuid,
            DT_CURRENTNODE  : startnode,
            DT_TICKETFERENCE : [ ticketreference ],
            DT_OWNER : ""
        }
    
    decisionThreadDatabase[threadUuid] = newThread
    
    # TODO: use execution engine for initial run until halt...
    
    return create_successful_uuid_result(threadUuid)
    