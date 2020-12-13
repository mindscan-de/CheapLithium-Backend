'''
Created on 12.12.2020

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


class KnowledgeBaseArticles(object):
    '''
    classdocs
    '''


    def __init__(self, knowledge_dir: str):
        '''
        Constructor
        '''
        self.__datamodel_directory = knowledge_dir
        self.__inMemoryDatabase = {}

        
    def _create_article_internal(self, pagetitle:str, pagecontent:str, pagesummary:str):
        kba_uuid = str(uid.uuid4())
        
        article = {
            KBA_UUID: 'KBA_'+kba_uuid,
            KBA_PAGETITLE: pagetitle,
            KBA_PAGESUMMARY: pagesummary,
            KBA_PAGECONTENT: pagecontent,
            KBA_REVISION: 1
            }
        
        return article, kba_uuid
    
    def insert_article(self, pagetitle:str, pagecontent:str, pagesummary:str):
        article, kba_uuid = self._create_article_internal(pagetitle, pagecontent, pagesummary)
        
        self.__inMemoryDatabase[kba_uuid] = article
        
        # TODO: save the article to disk
        
        return article, kba_uuid
        
    def select_article_by_uuid(self, kba_uuid:str):
        if kba_uuid not in self.__inMemoryDatabase:
            # TODO: try to laod article from disk, otherwise
            article, _ = self._create_article_internal("Unknown title / Unknown article", "This knowledgebase article doesn't exist. No such UUID in knowledge_base.", "Error retrieving article content")
            return article
        
        return self.__inMemoryDatabase[kba_uuid]
    
    def update_article_where_uuid(self, kba_uuid:str, pagetitle:str, pagecontent:str, pagesummary:str ):
        article = self.select_article_by_uuid(kba_uuid)
        
        article[KBA_PAGETITLE] = pagetitle
        article[KBA_PAGECONTENT] = pagecontent
        article[KBA_PAGESUMMARY] = pagesummary
        article[KBA_REVISION] = 1 + article[KBA_REVISION]
        
        self.__inMemoryDatabase[kba_uuid] = article
        
        # TODO: save the article to disk
        
        return article, kba_uuid
    
    def select_all_from_article(self):
        result_list = []
        for key, value in self.__inMemoryDatabase.items():
            result_list.append({
                    KBA_UUID : key,
                    KBA_PAGETITLE : value[KBA_PAGETITLE],
                    KBA_REVISION : value[KBA_REVISION],
                    KBA_PAGESUMMARY : value[KBA_PAGESUMMARY]
                });
                
        # TODO: order by pagetitle
        return {'result':result_list}
    