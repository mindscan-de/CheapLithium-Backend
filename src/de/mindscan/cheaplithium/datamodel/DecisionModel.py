'''
Created on 11.12.2020

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
import uuid as uid

from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport


# I currently do not like, that this thing is having too much responsibilities
# but it is still better than having these in the webserver code directly.
# better but is not good enough -> have to refactor this later


class DecisionModel(object):
    '''
    classdocs
    '''


    def __init__(self, datamodel_dir = ''):
        '''
        Constructor
        '''
        self.__datamodel_directory = datamodel_dir
        self.__inMemoryDatabase = {}
        
        
    def create_decision_node_transition_internal(self, name, nextnodeuuid, template):
        return { 
            DNT_NAME: name, 
            DNT_NEXT: nextnodeuuid, 
            DNT_TEMPLATE: template }

    def create_decision_node_internal(self, dnname, dntype, kbarticle, dnfollownodes):
        dnUuid = str(uid.uuid4())
        decisionNode = {
            DN_UUID: 'DN_' + dnUuid, 
            DN_NAME: dnname , 
            DN_TYPE: dntype , 
            DN_KBARTICLE: kbarticle ,
            DN_NEXTACTIONS: []}
        
        if len(dnfollownodes) >= 1:
            if(len(dnfollownodes)) == 1:
                tn = self.create_decision_node_transition_internal(
                    'default', dnfollownodes[0][DN_UUID], '')
                decisionNode[DN_NEXTACTIONS].append(tn)
            else:
                # TODO: if more then do something else
                pass
        
        return decisionNode, dnUuid
    
    def create_decision_model_internal(self, name:str, displayname:str, description:str, version:str):
        dmUuid = str(uid.uuid4())
        
        endnode, _ = self.create_decision_node_internal('900.endstate',DN_TYPE_END,'',[])  
        startnode, _ = self.create_decision_node_internal('000.startstate',DN_TYPE_START,'',[endnode])
    
        decisionModel = {
            DM_UUID: 'DM_' + dmUuid, 
            DM_NAME: name, 
            DM_DISPLAYNAME: displayname, 
            DM_VERSION: version, 
            DM_DESCRIPTION: description, 
            DM_STARTNODE: startnode[DN_UUID],
            DM_NODES: [startnode, endnode]}
        
        self.__inMemoryDatabase[dmUuid] = decisionModel
        
        return  decisionModel, dmUuid
    
    def insert_decision_node_into_decision_model(self, dn, dmuuid:str):
        decisionModel = self.__inMemoryDatabase[dmuuid]
        
        nodes = decisionModel[DM_NODES]
        nodes.append(dn)
        #  sort decision nodes by name (good enough) 
        sortednodes = sorted(nodes, key=lambda k: k['name'])
        decisionModel[DM_NODES] = sortednodes
         
        self.__inMemoryDatabase[dmuuid] = decisionModel
        
        return decisionModel, dmuuid
    
    def isInDatabase(self, uuid):
        return uuid in self.__inMemoryDatabase
    
    def insert_decision_node_transition_internal(self, uuid, dnuuid, transitionObject):
        decisionModel = self.__inMemoryDatabase[uuid]
        for decisionNode in decisionModel[DM_NODES]:
            if decisionNode[DN_UUID] == dnuuid:
                decisionNode[DN_NEXTACTIONS].append(transitionObject)
                return
    
    def update_decision_node_transitrion_internal(self, uuid, dnuuid, index, transitionObject):
        decisionModel = self.__inMemoryDatabase[uuid]
        for decisionNode in decisionModel[DM_NODES]:
            if decisionNode[DN_UUID] == dnuuid:
                decisionNode[DN_NEXTACTIONS][index] = transitionObject
                return

    
    # TODO: refactor that into file backend (later).
    def persist_decision_model_internal(self, dmuuid):
        jsonfilepath = self.__datamodel_directory + dmuuid + '.json'
        
        with open(jsonfilepath,"w") as json_target_file:
            json.dump(self.__inMemoryDatabase[dmuuid], json_target_file,indent=2);

    def provide_decision_model_internal(self, uuid:str):
        
        if uuid in self.__inMemoryDatabase:
            return self.__inMemoryDatabase[uuid]
        else:
            jsonfilepath = self.__datamodel_directory + uuid + '.json'
            if os.path.isfile(jsonfilepath):
                with open(jsonfilepath) as json_source_file:
                    tmpDecisionModel = json.load(json_source_file)
                    self.__inMemoryDatabase[uuid] = tmpDecisionModel
                    return tmpDecisionModel
            else:
                return {"message":"no_such_persisted_model "}


    # TODO: implement the listing by crawling the keys of the Database and join it with the filenames of the directory.
    #       also skip files, which keys are already present in the list -> no deseialization needed.
    #       in future use a database and use SQL and/or NOSQL, but for this approach, we really don't need a database at this stage.

    def select_decision_models_from_backend(self):
        # 2020-11-29:
        # this is just a crude hack, but there is no reason to implement an index of the models right now.
        # ... only want to bootstrap something else right now. no need to implement a solution at the moment 
        return  {
            "items": [
                {
                    DM_UUID: "0518f24f-41a0-4f13-b5f6-94a015b5b04c",
                    DM_NAME: "MyGlasswallDecisionModel",
                    DM_DISPLAYNAME: "My Glasswall Decision Model",
                    DM_VERSION: "1.0",
                    DM_DESCRIPTION:"This model helps to analyze issues generated by me - Glasswall"
                },
                {
                    DM_UUID: "bfb2e592-bd77-433e-8ea7-9e630939ae72", 
                    DM_NAME: "MyModel", 
                    DM_DISPLAYNAME: "My Model is best Model", 
                    DM_VERSION: "1.0", 
                    DM_DESCRIPTION: "This Model will make you smarter. Promised!"                
                },
                {
                    DM_UUID: "fa4c1a38-26f3-41c7-be76-bee7b2e0e9cb", 
                    DM_NAME: "MyModel", 
                    DM_DISPLAYNAME: "This is only my decond best mdel", 
                    DM_VERSION: "2.0", 
                    DM_DESCRIPTION: "But this will make you even more smarter."
                },
                {
                    DM_UUID: "db60a6a3-97c6-4f51-8513-b4751c650eb4", 
                    DM_NAME: "ChoosingTheRightEstimator", 
                    DM_DISPLAYNAME: "Choosing the right Estimator", 
                    DM_VERSION: "1.0", 
                    DM_DESCRIPTION: "Often the hardest part of solvind a machine learning problem can be finding the right estimator for the job.\r\nDifferent estimators are better suited for different types of data and differen problems.\r\nThe decision tree is designed to give usera a bit of a rough guide on how to approach problems with regard to which estimators to try on your data."
                } 
                ]}
