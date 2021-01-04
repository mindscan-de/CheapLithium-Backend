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

import os
import json
import uuid as uid

from fastapi import FastAPI, Form, HTTPException
from starlette.responses import FileResponse


app = FastAPI()

# import the data model column names / property names
from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport
# import the data tables / access to data on a amore abstract level 
from de.mindscan.cheaplithium.datamodel.DecisionModel import DecisionModel
from de.mindscan.cheaplithium.datamodel.DecisionThread import DecisionThread
from de.mindscan.cheaplithium.datamodel.DecisionThreadEnvironments import DecisionThreadEnvironments
from de.mindscan.cheaplithium.datamodel.KnowledgeBaseArticles import KnowledgeBaseArticles
from de.mindscan.cheaplithium.generator.ExportModelGenerator import ExportModelGenerator
from de.mindscan.cheaplithium.generator.ThreadReportGenerator import ThreadReportGenerator
from de.mindscan.cheaplithium.runtime.DecisionExecutionEngine import DecisionExecutionEngine

DATAMODEL_DIR = DATA_BASE_DIR + '/cheaplithium/dm/'
DATATHREAD_DIR = DATA_BASE_DIR + '/cheaplithium/threads/'
DATATHREADENV_DIR = DATA_BASE_DIR + '/cheaplithium/threads/env/'
KNOWLEDGE_DIR = DATA_BASE_DIR + '/cheaplithium/kb/';

# -----------------------------------------
# DecisionModel "Database"
# -----------------------------------------
 
decisionModels = DecisionModel(DATAMODEL_DIR)
decisionModels.load_all_models()

decisionThreads = DecisionThread(DATATHREAD_DIR)
decisionThreads.load_all_threads()

decisionThreadEnvironments = DecisionThreadEnvironments(DATATHREADENV_DIR)

knowledgeArticles = KnowledgeBaseArticles(KNOWLEDGE_DIR) 
knowledgeArticles.load_all_acrticles()

# -----------------------------------------
# Decision Execution Engine
# -----------------------------------------

decisionExecutionEngine = DecisionExecutionEngine(decisionModels, decisionThreads, decisionThreadEnvironments)

# -----------------------------------------
# Later extract the decision modelling code
# -----------------------------------------
def create_successful_uuid_result(uuid:str):
    return {"uuid":uuid, "isSuccess":True, "isError":False}

def strip_uuid(uuid):
    if(uuid.startswith("DM_") or uuid.startswith("DN_")) :
        return uuid[3:]
    else:
        if(uuid.startswith("KBA_")):
            return uuid[4:]
    return uuid

# -----------------------------------------
# Some basic input validation code.
# -----------------------------------------

def validate_uuid(uuid):
    try:
        read_uuid = str(uid.UUID('{' + uuid + '}'))
        if read_uuid == uuid:
            return read_uuid
        else:
            raise HTTPException(status_code=404, detail="Invalid uuid")
    except:
        raise HTTPException(status_code=404, detail="Invalid uuid")

def verify_dm_uuid(uuid):
    if not decisionModels.isInDatabase(uuid):
        raise HTTPException(status_code=404, detail="UUID not in database")
    
    return uuid
# --------------------------------------
# API-Webserver "code" - 
# --------------------------------------

@app.get("/")
def read_root():
    return {"message":"Hello World! It works! But now, go away!"}


@app.get("/CheapLithium/rest/getDecisionModel/{uuid}")
async def provide_decision_model( uuid:str):
    validate_uuid(uuid)
    
    model = decisionModels.select_decision_model_by_uuid(uuid)
    if model is None:
        raise HTTPException(status_code=404, detail="UUID not in database")
    else:
        return model


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
    dmuuid = verify_dm_uuid ( validate_uuid( strip_uuid(uuid) ) )

    decisionModels.persist_decision_model_internal(dmuuid)
        
    return create_successful_uuid_result(dmuuid)


@app.get("/CheapLithium/rest/getDecisionModelList")
async def get_decision_model_list():
    return decisionModels.select_decision_models_from_backend()
    

@app.post("/CheapLithium/rest/insertDecisionNodeTransition")
async def insert_decision_node_transition(uuid: str = Form(...), dnuuid:str=Form(...), transition:str=Form(...)):
    transitionObject = json.loads(transition)
    
    uuid = verify_dm_uuid( validate_uuid( strip_uuid(uuid) ) )
    
    decisionModels.insert_decision_node_transition_internal(uuid, dnuuid,  transitionObject)
    
    return create_successful_uuid_result(uuid)


@app.post("/CheapLithium/rest/updateDecisionNodeTransition")
async def update_decision_node_transition(uuid: str = Form(...), dnuuid:str=Form(...), index:int=Form(...), transition:str=Form(...)):
    transitionObject = json.loads(transition)

    uuid = verify_dm_uuid( validate_uuid( strip_uuid(uuid) ) )
    
    decisionModels.update_decision_node_transitrion_internal(uuid, dnuuid, index, transitionObject)
    
    return create_successful_uuid_result(uuid)
          

@app.post("/CheapLithium/rest/updateDecisionNode")
async def update_decision_node( uuid:str=Form(...), dnuuid:str=Form(...), name:str=Form(...), exectype:str=Form(...), kbarticle:str=Form(""), nodeaction:str=Form("")):
    uuid = verify_dm_uuid( validate_uuid( strip_uuid(uuid) ) )
    
    decisionModels.update_decision_node_internal(uuid, dnuuid, name, exectype, kbarticle, nodeaction)
        
    return create_successful_uuid_result(uuid)


@app.post("/CheapLithium/rest/updateDecisionModel")
async def update_decision_model(uuid: str = Form(...), name:str = Form(...),  displayname:str=Form(...), 
    description:str=Form(...), version:str = Form(...)):
    
    uuid = verify_dm_uuid( validate_uuid( strip_uuid(uuid) ) )
    
    decisionModels.update_decision_model_internal(uuid, name, displayname, description, version)
    
    return create_successful_uuid_result(uuid)

@app.post("/CheapLithium/rest/updateDecisionModelStartData")
async def update_decision_model_start_configuration(uuid:str=Form(...), startnode:str=Form(...), startenvironment:str=Form("")):
    uuid = verify_dm_uuid( validate_uuid( strip_uuid(uuid)) )
    
    decisionModels.update_start_configuration(uuid, startnode, startenvironment)
    
    return create_successful_uuid_result(uuid)

@app.get("/CheapLithium/rest/exportModelXGML/{uuid}")
def export_model_as_xgml(uuid:str):
    uuid = verify_dm_uuid( validate_uuid( strip_uuid(uuid) ) )
    
    generator = ExportModelGenerator(decisionModels)
    fullpath = generator.exportAsYEDML(uuid)
    if os.path.isfile(fullpath):
        _, file_name = os.path.split(fullpath)
        return FileResponse(fullpath,media_type='application/octet-stream',filename=file_name)
    
    raise HTTPException(status_code=404, detail="Item not found")
    
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
async def provide_decision_thread(uuid: str):
    uuid = validate_uuid(uuid)
        
    thread = decisionThreads.select_decision_thread_by_uuid(uuid)
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    else:
        return thread


@app.get("/CheapLithium/rest/getDecisionThreadList")
async def get_decision_thread_list():
    return decisionThreads.select_all_from_decision_threads()


@app.post("/CheapLithium/rest/startDecisionThread")
async def create_decision_thread(uuid:str=Form(...), ticketreference:str = Form("")):
    dmuuid = validate_uuid( strip_uuid(uuid) )
    
    thread_uuid = decisionExecutionEngine.start_decision_thread_by_model_uuid(dmuuid, ticketreference)

    if thread_uuid is None:
        return {"message":"no such model or something else"}

    decisionExecutionEngine.process_single_decision_thread(thread_uuid)

    return create_successful_uuid_result(thread_uuid)


@app.get("/CheapLithium/rest/getDecisionThreadReport/{uuid}")
async def get_decision_thread_report(uuid:str):
    thread_uuid = validate_uuid( strip_uuid(uuid) )
    
    reportGenerator = ThreadReportGenerator(decisionThreads, decisionModels, decisionThreadEnvironments)
    result = reportGenerator.generate_thread_report(thread_uuid);
    if result is not None:
        return result 
    

##
##
## KnowledgeBase-Articles
##
##

@app.get("/CheapLithium/rest/getKBArticlesList")
async def get_kb_articles_list():
    return knowledgeArticles.select_all_from_article()

@app.get("/CheapLithium/rest/getKBArticle/{uuid}")
async def provide_kbarticle(uuid:str):
    uuid = validate_uuid( strip_uuid(uuid) )
    
    return knowledgeArticles.select_article_by_uuid(uuid)

@app.post("/CheapLithium/rest/insertKBArticle")
async def create_kbarticle(pagetitle:str=Form(...), pagesummary:str=Form(""), pagecontent:str=Form(...)):
    _, kba_uuid = knowledgeArticles.insert_article(pagetitle, pagecontent, pagesummary)
    
    return create_successful_uuid_result(kba_uuid)

@app.post("/CheapLithium/rest/updateKBArticle")
async def update_kbarticle(uuid:str=Form(...), pagetitle:str=Form(...), pagesummary:str=Form(""), pagecontent:str=Form(...)):
    uuid = validate_uuid( strip_uuid(uuid) )

    knowledgeArticles.update_article_where_uuid(uuid, pagetitle, pagecontent, pagesummary)
    return create_successful_uuid_result(uuid)
