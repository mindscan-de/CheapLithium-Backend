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
import uuid as uid

from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport

class DecisionModel(object):
    '''
    classdocs
    '''


    def __init__(self, datamodel_dir = ''):
        '''
        Constructor
        '''
        self.__datamodel_directory = datamodel_dir
        
        
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
