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

# -----------------------------------------
# Data Model property names
# -----------------------------------------

# Internal Model of the Decision Model
DM_NODES       = 'nodes'
DM_NAME        = 'name'
DM_UUID        = 'uuid'
DM_DISPLAYNAME = 'displayname'
DM_DESCRIPTION = 'description'
DM_STARTNODE   = 'startnode'
DM_VERSION     = 'version'

# Internal Model of the Decision Node
DN_UUID        = 'uuid'
DN_NAME        = 'name'
DN_TYPE        = 'type'
DN_TYPE_END    = 'end'
DN_TYPE_START  = 'start'
DN_TYPE_HIT    = 'hit'
DN_TYPE_MIT    = 'mit'
DN_KBARTICLE   = 'kbarticle'
DN_NEXTACTIONS = 'nextactions'

# Internal Model of the Decision Node Transition
DNT_NAME       = 'name'
DNT_NEXT       = 'next'
DNT_TEMPLATE   = 'template'

# internal Model of the Knowledge Base 
KBA_UUID        = 'uuid'
KBA_PAGETITLE   = 'pagetitle'
KBA_PAGECONTENT = 'pagecontent'
KBA_PAGESUMMARY = 'pagesummary'
KBA_REVISION    = 'revision'
KBA_CREATED     = 'created'
KBA_MODIFIED    = 'modified' 

#incternal Model of the Decision Thread
DT_UUID          = 'uuid'
DT_ENVIRONMENT   = 'environment'
DT_CURRENTSTATE  = 'currentstate'
DT_CURRENTMODEL  = 'currentmodel'
DT_CURRENTNODE   = 'currentnode' 
DT_TICKETFERENCE = 'ticketreference'
DT_CREATED       = 'created'
DT_MODIFIED      = 'modified'
DT_FINALIZED     = 'finalized' 
DT_OWNER         = 'owner'

RT_STATE_STARTED    = 'STARTED'
RT_STATE_STOPPED    = 'STOPPED'
RT_STATE_BLOCKED    = 'BLOCKED'
RT_STATE_WAIT_FOR_TRANSIT = 'WAITFORTRANSIT'
RT_STATE_TERMINATED = 'TERMINATED'
