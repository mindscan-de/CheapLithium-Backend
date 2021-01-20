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

__local_engine = None


## TODO something like this to inject user data back into the input evaluation, without cripling the interpreter
def __inject_engine(engine):
    __local_engine = engine

## according to the 
def user_textfield(label, description):
    if __local_engine.__isrenderui_mode:
        # TODO: maybe write that back into the engine
        # return the UI - rendering instructions
        return \
            {
                'label' : label,
                'type' : 'textfield',
                'description' : description 
            }
    else:
        # return the real input of the user
        return __local_engine.__input_data[label]
        
def user_textarea(label, description):
    if __local_engine.__isrenderui_mode:
        # TODO: maybe write that back into the engine
        # return the UI - rendering instructions
        return \
            {
                'label' : label,
                'type' : 'textarea',
                'description' : description 
            }
    else:
        return __local_engine.__input_data[label]

def user_yesnoselection(label, description):
    # TODO: maybe write that back into the engine
    if __local_engine.__isrenderui_mode:
        return \
            {
                'label' : label,
                'type' : 'yesnoselection',
                'description' : description 
            }
    else:
        return __local_engine.__input_data['label']
