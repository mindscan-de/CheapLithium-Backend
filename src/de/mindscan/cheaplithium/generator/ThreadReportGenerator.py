'''
Created on 21.12.2020

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

from de.mindscan.cheaplithium.datamodel.DecisionModel import DecisionModel
from de.mindscan.cheaplithium.datamodel.DecisionThread import DecisionThread
from de.mindscan.cheaplithium.datamodel.DecisionThreadEnvironments import DecisionThreadEnvironments


class ThreadReportGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, decisionThreads:DecisionThread, decisionModels:DecisionModel, threadEnvironments:DecisionThreadEnvironments):
        '''
        Constructor
        '''
        self.__threadProvider = decisionThreads
        self.__modelProvider = decisionModels
        self.__environmentProvider = threadEnvironments
        
    def generate_thread_report(self, thread_uuid):
        # load thread from thread_uuid using threadProvider
        # read environment uuid from thread
        # load environment from environment_uuid using environmentProvider
        # collect execution report from thread_environment
        # laod model uuid from thread
        # load model from model_uuid using modelProvider
        
        # now use model, report, environment(?), and thread(?) to generate a report
        # the result report contains a list of detailreports for each node/transition
        # the result is a dictionary of 'reportitems' => [{},{}]
        # the user can then select the reportitems for the report
        
        return None
    
    