'''
Created on 19.12.2020

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


# import the data model column names / property names
from de.mindscan.cheaplithium.datamodel.consts import *  # @UnusedWildImport
# import the data tables / access to data on a amore abstract level
from de.mindscan.cheaplithium.datamodel.DecisionModel import DecisionModel


class ExportModelGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, decisionModelDataProvider:DecisionModel):
        '''
        Constructor
        '''
        self.__modelDataProvider = decisionModelDataProvider

    # idea is: 
    # * create a yml file each time this is called
    # * then return the path of the file
    # * then let the webserver serve that file for download 
    def exportAsYEDML(self, dmUUID:str):
        exportPath = self.__modelDataProvider.get_data_model_directory()
        filename = dmUUID + ".export.xgml"
        
        joinedPath = os.path.join(exportPath,filename)
        with open(joinedPath,'w') as document:
            # collect nodes from the model
            model = self.__modelDataProvider.select_decision_model_by_uuid(dmUUID)
            self._write_document(document, model)
            document.flush()
        
        return joinedPath
    
    def _write_document(self, document, model):
        # don't know whether i should support utf-8 or something, but this is Windows Codepage 1252 for now
        document.write('<?xml version="1.0" encoding="Cp1252"?>')
        document.write('<section name="xgml">')
        document.write('    <attribute key="Creator" type="String">yFiles</attribute>')
        document.write('    <attribute key="Version" type="String">2.17</attribute>')

        self._write_graph_section(document, model)
        
        document.write('</section>')
    
    def _write_graph_section(self, document, model):
        document.write('    <section name="graph">')
        document.write('        <attribute key="hierarchic" type="int">1</attribute>')
        document.write('        <attribute key="label" type="String"></attribute>')
        document.write('        <attribute key="directed" type="int">1</attribute>')
        node_translation = self._write_nodes(document, model)
        # write transitions
        self._write_edges(document, model, node_translation)
        document.write('    </section>')

            
    def _write_nodes(self, document, model):
        node_translation = {}
        for idx, node in enumerate(model[DM_NODES], start=0):
            node_translation[node[DN_UUID]] = idx
            self._write_single_node(document, node, idx)
            
        # return a dictionary for node-uuids to index translations
        return node_translation

    
    def _write_single_node(self, document, node, index):
        document.write('        <section name="node">')
        document.write('            <attribute key="id" type="int">{}</attribute>'.format(index));
        document.write('            <attribute key="label" type="String">{}</attribute>'.format(node[DN_NAME]))
        document.write('            <section name="graphics">')
        # TODO: simple layout and stuch stuff x,y
        document.write('                <attribute key="x" type="double">250.0</attribute>')
        document.write('                <attribute key="y" type="double">{}</attribute>'.format(100 + 100*index))
        # TODO: calculate/extimate width / height of box
        document.write('                <attribute key="w" type="double">200.0</attribute>')
        document.write('                <attribute key="h" type="double">50.0</attribute>')
        document.write('                <attribute key="type" type="String">rectangle</attribute>')
        document.write('                <attribute key="raisedBorder" type="boolean">false</attribute>')
        # TODO use colorcoded boxes for hit, mit, sync, start, end, etc nodes
        document.write('                <attribute key="fill" type="String">#FF6600</attribute>')
        document.write('                <attribute key="outline" type="String">#000000</attribute>')
        document.write('            </section>')
        document.write('            <section name="LabelGraphics">')
        document.write('                <attribute key="text" type="String">{}</attribute>'.format(node[DN_NAME]))
        document.write('                <attribute key="fontSize" type="int">12</attribute>')
        document.write('                <attribute key="fontName" type="String">Dialog</attribute>')
        document.write('                <attribute key="model"/>')
        document.write('            </section>')
        document.write('        </section>')
    
    def _write_edges(self, document, model, node_translation):
        # TODO: foreach node, foreach transiton in each node
        for idx, node in enumerate(model[DM_NODES], start=0):
            #write_edge
            pass
        pass
    
    def _write_single_edge(self, document, data):
        document.write('        <section name="edge">')
        # TODO: source, target, label, section:graphics section, section:LabelGraphics
        document.write('        </section>')
