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
        
        # collect nodes from the model
        # write document header (preamble)
        # write nodes
        # write transitions
        # write document end (postamble)
        
        # TODO: return the full file path.
        pass
    
    def _write_document(self, document, data):
        with document:
            document.write('<?xml version="1.0" encoding="Cp1252"?>')
            document.write('<section name="xgml">')
            document.write('    <attribute key="Creator" type="String">yFiles</attribute>')
            document.write('    <attribute key="Version" type="String">2.17</attribute>')
            self._write_graph_section(document, data)
            document.write('</section>')
    
    def _write_graph_section(self, document, data):
        with document:
            document.write('    <section name="graph">')
            document.write('        <attribute key="hierarchic" type="int">1</attribute>')
            document.write('        <attribute key="label" type="String"></attribute>')
            document.write('        <attribute key="directed" type="int">1</attribute>')
            
            self._write_nodes(self, document, data)
            self._write_edges(self, document, data)
            
            document.write('    </section>')
            
    def _write_nodes(self, document, data):
        # TODO: foreach node
        # node id is zero based
        #          write node
        #          collect transition
        pass
    
    def _write_single_node(self, document, data):
        with document:
            document.write('        <section name="node">')
            # TODO: id, label, section:label, section:LabelGraphics
            document.write('        </section>')
        pass
    
    def _write_edges(self, document, data):
        # TODO: foreach node, foreach transiton in each node
        #          write_edge
        pass
    
    def _write_single_edge(self, document, data):
        with document:
            document.write('        <section name="edge">')
            # TODO: source, target, label, section:graphics section, section:LabelGraphics
            document.write('        </section>')
        pass
