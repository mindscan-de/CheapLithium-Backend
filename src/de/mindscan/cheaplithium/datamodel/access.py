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
from de.mindscan.cheaplithium.datamodel.HashMap import HashMap


## ------------------------------------------------------------------------------------
## MODEL FILE BACKEND
## ------------------------------------------------------------------------------------
## extract that to some kind of data backend.... / backend is first somethin file based
## ------------------------------------------------------------------------------------
def backend_load_decision_model(uuid:str):
    # check if file exists
    # if file not exists raise exception
    # otherwise load content and return content
    return {'backenddata':'success'}




## The decisionModelMap / decisionModelDatabase
decisionModelMap = HashMap(None)

## this should be a more readable interface
def get_decision_model(uuid:str):
    global decisionModelMap
    return decisionModelMap.computeIfAbsent(uuid, backend_load_decision_model )


