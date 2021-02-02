'''
Created on 20.01.2021

MIT License

Copyright (c) 2021 Maxim Gansert

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
from de.mindscan.cheaplithium.parser.SpecialEngine import SpecialEngine 

__input__local_engine = SpecialEngine()

def _inject_engine(engine:SpecialEngine):
    global __input__local_engine
    if engine is None:
        __input__local_engine = SpecialEngine()
    else:
        __input__local_engine = engine

 
def textfield(label:str, description:str):
    global __input__local_engine
    if __input__local_engine.isInterfaceRenderMode():
        item = {
            'label' : label,
            'type' : 'textfield',
            'description' : description 
            }
        __input__local_engine.appendInputInterface(item)
        return item
    else:
        return __input__local_engine.getUserLabelledInput(label)
    

def textfield_int(label:str, description:str):
    global __input__local_engine
    if __input__local_engine.isInterfaceRenderMode():
        item = {
            'label' : label,
            'type' : 'textfield',
            'description' : description 
            }
        __input__local_engine.appendInputInterface(item)
        return item
    else:
        return int(__input__local_engine.getUserLabelledInput(label).strip())
    
        
        
def textarea(label:str, description:str):
    global __input__local_engine
    if __input__local_engine.isInterfaceRenderMode():
        item = {
            'label' : label,
            'type' : 'textarea',
            'description' : description
            }
        __input__local_engine.appendInputInterface(item)
        return item
    else:
        return __input__local_engine.getUserLabelledInput(label)


def yesno(label:str, description:str):
    global __input__local_engine
    if __input__local_engine.isInterfaceRenderMode():
        item = {
            'label' : label,
            'type' : 'yesnoselection',
            'description' : description 
            }
        __input__local_engine.appendInputInterface(item)
        return item
    else:
        return __input__local_engine.getUserLabelledInput(label)
